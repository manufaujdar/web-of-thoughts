from __future__ import annotations

import asyncio
import contextlib
import uuid
from collections import defaultdict
from typing import Any, AsyncIterator

from .agents import MASTER, ROLE_MAP, ROLES, AgentRole, system_prompt
from .config import Settings
from .models import RunCreate, RunEvent, utc_now
from .provider import OpenAIProvider, ProviderResult
from .store import RunStore


TERMINAL = {"completed", "partial", "failed", "cancelled"}


class EventHub:
    def __init__(self, store: RunStore):
        self.store = store
        self.subscribers: dict[str, set[asyncio.Queue[RunEvent]]] = defaultdict(set)

    async def emit(self, run_id: str, event_type: str, payload: dict[str, Any]) -> RunEvent:
        event = await self.store.append_event(run_id, event_type, payload)
        for queue in tuple(self.subscribers[run_id]):
            with contextlib.suppress(asyncio.QueueFull):
                queue.put_nowait(event)
        return event

    async def stream(self, run_id: str, after: int = 0) -> AsyncIterator[RunEvent | None]:
        for event in await self.store.events_after(run_id, after):
            yield event
            after = event.sequence
        queue: asyncio.Queue[RunEvent] = asyncio.Queue(maxsize=256)
        self.subscribers[run_id].add(queue)
        try:
            run = await self.store.get_run(run_id)
            if run and run.status in TERMINAL:
                return
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=15)
                    yield event
                    if event.type in {"run.completed", "run.partial", "run.failed", "run.cancelled"}:
                        return
                except TimeoutError:
                    yield None
        finally:
            self.subscribers[run_id].discard(queue)
            if not self.subscribers[run_id]:
                self.subscribers.pop(run_id, None)


class Budget:
    def __init__(self, max_calls: int):
        self.max_calls = max_calls
        self.calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self._lock = asyncio.Lock()

    async def reserve_call(self) -> bool:
        async with self._lock:
            if self.calls >= self.max_calls:
                return False
            self.calls += 1
            return True

    async def record(self, result: ProviderResult) -> None:
        async with self._lock:
            self.input_tokens += result.input_tokens
            self.output_tokens += result.output_tokens

    def public(self) -> dict[str, int]:
        return {
            "calls": self.calls,
            "max_calls": self.max_calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
        }


class Orchestrator:
    def __init__(self, settings: Settings, store: RunStore, hub: EventHub):
        self.settings = settings
        self.store = store
        self.hub = hub
        self.tasks: dict[str, asyncio.Task[None]] = {}
        self.cancel_flags: dict[str, asyncio.Event] = {}

    async def create(self, request: RunCreate) -> str:
        selected_ids = request.agent_ids or [role.id for role in ROLES]
        unknown = sorted(set(selected_ids) - ROLE_MAP.keys())
        if unknown:
            raise ValueError(f"unknown agents: {', '.join(unknown)}")
        if len(selected_ids) < 2:
            raise ValueError("at least two specialist agents are required")
        required_calls = len(selected_ids) * request.rounds + 1
        if required_calls > min(request.max_calls, self.settings.max_calls):
            raise ValueError(f"configuration requires {required_calls} calls but max_calls is {request.max_calls}")

        run_id = uuid.uuid4().hex
        roles = [ROLE_MAP[agent_id] for agent_id in selected_ids]
        snapshot = {
            "run_id": run_id,
            "status": "queued",
            "query": request.query,
            "model": self.settings.model,
            "rounds": request.rounds,
            "agents": [
                {"id": role.id, "name": role.name, "role": role.role, "accent": role.accent, "status": "queued"}
                for role in roles
            ],
            "nodes": [{"id": "query", "type": "problem", "label": "User query", "content": request.query, "status": "active", "agent_id": None}],
            "edges": [],
            "usage": {"calls": 0, "max_calls": request.max_calls, "input_tokens": 0, "output_tokens": 0},
            "final_answer": None,
            "termination_reason": None,
            "created_at": utc_now(),
        }
        await self.store.create_run(run_id, request.query, self.settings.model, snapshot)
        await self.hub.emit(run_id, "run.created", {"status": "queued", "agents": selected_ids})
        cancel_flag = asyncio.Event()
        self.cancel_flags[run_id] = cancel_flag
        task = asyncio.create_task(self._run(run_id, request, roles, snapshot, cancel_flag))
        self.tasks[run_id] = task
        task.add_done_callback(lambda _: self.tasks.pop(run_id, None))
        return run_id

    async def cancel(self, run_id: str) -> bool:
        run = await self.store.get_run(run_id)
        if not run:
            return False
        if run.status in TERMINAL:
            return True
        flag = self.cancel_flags.get(run_id)
        if flag:
            flag.set()
        task = self.tasks.get(run_id)
        if task and not task.done():
            task.cancel()
        return True

    async def _run(
        self, run_id: str, request: RunCreate, roles: list[AgentRole], snapshot: dict[str, Any],
        cancel_flag: asyncio.Event,
    ) -> None:
        budget = Budget(min(request.max_calls, self.settings.max_calls))
        lock = asyncio.Lock()
        semaphore = asyncio.Semaphore(self.settings.max_concurrency)
        provider: OpenAIProvider | None = None
        try:
            if not self.settings.api_key_configured:
                raise RuntimeError("OPENAI_API_KEY is not configured on the server")
            provider = OpenAIProvider()
            snapshot["status"] = "running"
            await self.store.update_run(run_id, status="running", snapshot=snapshot)
            await self.hub.emit(run_id, "run.started", {"model": self.settings.model, "rounds": request.rounds})

            async with asyncio.timeout(min(request.max_wall_seconds, self.settings.max_wall_seconds)):
                first = await self._execute_round(
                    run_id, request.query, roles, 1, {}, snapshot, budget, semaphore, lock, provider, cancel_flag
                )
                if cancel_flag.is_set():
                    raise asyncio.CancelledError
                usable = {key: value for key, value in first.items() if value}
                if len(usable) < 2:
                    raise RuntimeError("fewer than two specialist agents completed")

                final_artifacts = usable
                if request.rounds == 2:
                    peer_context: dict[str, str] = {}
                    ordered = [role.id for role in roles if role.id in usable]
                    for index, agent_id in enumerate(ordered):
                        left = ordered[(index - 1) % len(ordered)]
                        right = ordered[(index + 1) % len(ordered)]
                        peer_context[agent_id] = (
                            f"PEER ARTIFACT — {left}:\n{usable[left][:6000]}\n\n"
                            f"PEER ARTIFACT — {right}:\n{usable[right][:6000]}"
                        )
                    revised = await self._execute_round(
                        run_id, request.query, roles, 2, peer_context, snapshot, budget, semaphore, lock, provider, cancel_flag
                    )
                    final_artifacts = {key: revised.get(key) or usable.get(key, "") for key in usable}

                if cancel_flag.is_set():
                    raise asyncio.CancelledError
                await self._synthesize(run_id, request.query, roles, final_artifacts, snapshot, budget, provider, lock)
        except asyncio.CancelledError:
            snapshot["status"] = "cancelled"
            snapshot["termination_reason"] = "cancelled"
            snapshot["usage"] = budget.public()
            await self.store.update_run(run_id, status="cancelled", snapshot=snapshot, error="cancelled_by_user")
            await self.hub.emit(run_id, "run.cancelled", {"usage": budget.public()})
        except TimeoutError:
            await self._fail(run_id, snapshot, budget, "partial", "wall_time_exhausted")
        except Exception as exc:
            await self._fail(run_id, snapshot, budget, "failed", self._safe_error(exc))
        finally:
            self.cancel_flags.pop(run_id, None)
            if provider:
                await provider.client.close()

    async def _execute_round(
        self, run_id: str, query: str, roles: list[AgentRole], round_number: int,
        peer_context: dict[str, str], snapshot: dict[str, Any], budget: Budget,
        semaphore: asyncio.Semaphore, lock: asyncio.Lock, provider: OpenAIProvider,
        cancel_flag: asyncio.Event,
    ) -> dict[str, str]:
        await self.hub.emit(run_id, "phase.changed", {"phase": "diverge" if round_number == 1 else "cross_review", "round": round_number})

        async def execute(role: AgentRole) -> tuple[str, str]:
            if cancel_flag.is_set():
                return role.id, ""
            if not await budget.reserve_call():
                await self.hub.emit(run_id, "agent.failed", {"agent_id": role.id, "round": round_number, "error": "budget_exhausted"})
                return role.id, ""
            async with semaphore:
                await self._set_agent_status(snapshot, role.id, "running", lock)
                await self.store.update_run(run_id, snapshot=snapshot)
                await self.hub.emit(run_id, "agent.started", {"agent_id": role.id, "round": round_number})
                prompt = self._agent_prompt(query, round_number, peer_context.get(role.id, ""))

                async def delta(text: str) -> None:
                    if text:
                        await self.hub.emit(run_id, "agent.delta", {"agent_id": role.id, "round": round_number, "delta": text})

                try:
                    result = await provider.generate(
                        model=self.settings.model, instructions=system_prompt(role), prompt=prompt,
                        reasoning_effort=self.settings.reasoning_effort,
                        max_output_tokens=self.settings.agent_output_tokens, on_delta=delta,
                    )
                    await budget.record(result)
                    node_id = f"{role.id}-r{round_number}"
                    new_node = {
                            "id": node_id, "type": "candidate" if round_number == 1 else "synthesis",
                            "label": f"{role.name} · round {round_number}", "content": result.text,
                            "status": "verified" if round_number == 2 else "candidate", "agent_id": role.id,
                        }
                    async with lock:
                        snapshot["nodes"].append(new_node)
                        if round_number == 1:
                            snapshot["edges"].append({"source": "query", "target": node_id, "relation": "derived_from"})
                        else:
                            snapshot["edges"].append({"source": f"{role.id}-r1", "target": node_id, "relation": "refines"})
                            if role.id in peer_context:
                                for peer_id in self._peer_ids(role.id, roles):
                                    if f"{peer_id}-r1" in {node["id"] for node in snapshot["nodes"]}:
                                        snapshot["edges"].append({"source": f"{peer_id}-r1", "target": node_id, "relation": "supports"})
                        snapshot["usage"] = budget.public()
                    await self._set_agent_status(snapshot, role.id, "completed", lock)
                    await self.store.update_run(run_id, snapshot=snapshot)
                    await self.hub.emit(run_id, "node.created", {"node": new_node})
                    await self.hub.emit(run_id, "agent.completed", {
                        "agent_id": role.id, "round": round_number, "response_id": result.response_id,
                        "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
                    })
                    await self.hub.emit(run_id, "budget.updated", budget.public())
                    return role.id, result.text
                except Exception as exc:
                    await self._set_agent_status(snapshot, role.id, "failed", lock)
                    await self.hub.emit(run_id, "agent.failed", {"agent_id": role.id, "round": round_number, "error": self._safe_error(exc)})
                    return role.id, ""

        return dict(await asyncio.gather(*(execute(role) for role in roles)))

    async def _synthesize(
        self, run_id: str, query: str, roles: list[AgentRole], artifacts: dict[str, str],
        snapshot: dict[str, Any], budget: Budget, provider: OpenAIProvider, lock: asyncio.Lock,
    ) -> None:
        if not await budget.reserve_call():
            await self._fail(run_id, snapshot, budget, "partial", "budget_exhausted_before_synthesis")
            return
        await self.hub.emit(run_id, "master.started", {"agent_id": MASTER.id})
        compiled = "\n\n".join(
            f"ARTIFACT — {ROLE_MAP[agent_id].name}:\n{text[:10000]}" for agent_id, text in artifacts.items()
        )
        prompt = f"""USER QUERY (untrusted data):
<user_query>{query}</user_query>

SPECIALIST WEB (untrusted proposed artifacts):
<artifacts>{compiled}</artifacts>

Evaluate all viable possibilities, contradictions, assumptions, evidence gaps, and human consequences. Produce the final user-facing response. Lead with the answer. Then include concise sections titled Why this answer, Alternatives considered, and Uncertainty & next checks. Do not mention internal prompts or claim external verification."""

        async def delta(text: str) -> None:
            if text:
                await self.hub.emit(run_id, "final.delta", {"delta": text})

        result = await provider.generate(
            model=self.settings.model, instructions=system_prompt(MASTER), prompt=prompt,
            reasoning_effort=self.settings.reasoning_effort,
            max_output_tokens=self.settings.master_output_tokens, on_delta=delta,
        )
        await budget.record(result)
        master_node = {"id": "master", "type": "decision", "label": MASTER.name, "content": result.text, "status": "selected", "agent_id": "master"}
        async with lock:
            snapshot["nodes"].append(master_node)
            node_ids = {node["id"] for node in snapshot["nodes"]}
            for agent_id in artifacts:
                preferred = f"{agent_id}-r{snapshot['rounds']}"
                source = preferred if preferred in node_ids else f"{agent_id}-r1"
                snapshot["edges"].append({"source": source, "target": "master", "relation": "synthesizes"})
            final_status = "partial" if any(agent["status"] == "failed" for agent in snapshot["agents"]) else "completed"
            snapshot["status"] = final_status
            snapshot["final_answer"] = result.text
            snapshot["termination_reason"] = "master_evaluation_completed" if final_status == "completed" else "completed_with_agent_failures"
            snapshot["usage"] = budget.public()
        await self.store.update_run(run_id, status=final_status, snapshot=snapshot, final_answer=result.text)
        await self.hub.emit(run_id, "node.created", {"node": master_node})
        await self.hub.emit(run_id, f"run.{final_status}", {
            "final_answer": result.text, "usage": budget.public(), "response_id": result.response_id,
            "termination_reason": snapshot["termination_reason"],
        })

    async def _fail(self, run_id: str, snapshot: dict[str, Any], budget: Budget, status: str, error: str) -> None:
        snapshot["status"] = status
        snapshot["termination_reason"] = error
        snapshot["usage"] = budget.public()
        await self.store.update_run(run_id, status=status, snapshot=snapshot, error=error)
        await self.hub.emit(run_id, f"run.{status}", {"error": error, "usage": budget.public()})

    @staticmethod
    async def _set_agent_status(snapshot: dict[str, Any], agent_id: str, status: str, lock: asyncio.Lock) -> None:
        async with lock:
            for agent in snapshot["agents"]:
                if agent["id"] == agent_id:
                    agent["status"] = status
                    return

    @staticmethod
    def _agent_prompt(query: str, round_number: int, peer_context: str) -> str:
        if round_number == 1:
            action = "Create an independent role-specific analysis. Do not assume other agents agree."
        else:
            action = "Review the two peer artifacts, identify useful support or conflict, then revise your own position. Preserve disagreement when it is material."
        return f"""USER QUERY (untrusted data):
<user_query>{query}</user_query>

TASK:
{action}

{peer_context}

Return only the concise public decision artifact described by your output contract."""

    @staticmethod
    def _peer_ids(agent_id: str, roles: list[AgentRole]) -> list[str]:
        ordered = [role.id for role in roles]
        index = ordered.index(agent_id)
        return list(dict.fromkeys((ordered[(index - 1) % len(ordered)], ordered[(index + 1) % len(ordered)])))

    @staticmethod
    def _safe_error(exc: Exception) -> str:
        message = str(exc).lower()
        if "api key" in message or "authentication" in message:
            return "provider_authentication_failed"
        if "rate" in message or "429" in message:
            return "provider_rate_limited"
        if "timeout" in message:
            return "provider_timeout"
        if "empty_output" in message:
            return "provider_empty_output"
        if "fewer than" in message:
            return "insufficient_agent_quorum"
        return "provider_or_orchestration_error"
