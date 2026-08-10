#!/usr/bin/env python3
"""Opt-in real OpenAI smoke test. This makes paid API calls and uses no mock provider."""

from __future__ import annotations

import asyncio
import os
import tempfile
from pathlib import Path

from wot_app.config import Settings
from wot_app.models import RunCreate
from wot_app.orchestrator import EventHub, Orchestrator
from wot_app.store import RunStore


async def run_smoke() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        print("NOT RUN: OPENAI_API_KEY is required for the real-provider smoke test.")
        return 2
    with tempfile.TemporaryDirectory(prefix="wot-live-") as directory:
        settings = Settings(
            model=os.environ.get("WOT_SMOKE_MODEL", os.environ.get("WOT_MODEL", "gpt-5.6-sol")),
            reasoning_effort="low",
            database_path=Path(directory) / "smoke.db",
            max_concurrency=2,
            max_calls=3,
            max_wall_seconds=180,
            agent_output_tokens=300,
            master_output_tokens=500,
        )
        store = RunStore(settings.database_path)
        await store.initialize()
        orchestrator = Orchestrator(settings, store, EventHub(store))
        run_id = await orchestrator.create(RunCreate(
            query="What are two practical ways to reduce food waste at home, and what tradeoff matters most?",
            agent_ids=["analyst", "skeptic"], rounds=1, max_calls=3, max_wall_seconds=180,
        ))
        await orchestrator.tasks[run_id]
        run = await store.get_run(run_id)
        assert run is not None
        assert run.status == "completed", f"unexpected terminal status: {run.status} ({run.error})"
        assert run.final_answer and len(run.final_answer) > 40
        assert run.snapshot["usage"]["calls"] == 3
        assert run.snapshot["usage"]["input_tokens"] + run.snapshot["usage"]["output_tokens"] > 0
        events = await store.events_after(run_id)
        assert sum(event.type == "run.completed" for event in events) == 1
        print(f"PASS: real run {run_id} completed with {len(events)} events and {run.snapshot['usage']}.")
        return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run_smoke()))
