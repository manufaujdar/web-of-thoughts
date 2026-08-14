from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from .agents import ROLES
from .config import Settings
from .models import AgentPublic, RunCreate
from .orchestrator import EventHub, Orchestrator
from .store import RunStore


settings = Settings.from_env()
store = RunStore(settings.database_path)
hub = EventHub(store)
orchestrator = Orchestrator(settings, store, hub)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await store.initialize()
    await store.prune_terminal_runs(settings.retention_days)
    yield
    for task in tuple(orchestrator.tasks.values()):
        task.cancel()
    if orchestrator.tasks:
        await asyncio.gather(*orchestrator.tasks.values(), return_exceptions=True)


app = FastAPI(title="Web of Thoughts API", version="0.2.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Last-Event-ID"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > 100_000:
                return Response(status_code=413)
        except ValueError:
            return Response(status_code=400)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; "
        "img-src 'self' data:; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
    )
    return response


@app.get("/health/live")
async def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
async def ready() -> dict[str, str | bool]:
    return {"status": "ready" if settings.api_key_configured else "configuration_required", "openai_configured": settings.api_key_configured}


@app.get("/api/v1/config")
async def config() -> dict:
    return {
        "model": settings.model,
        "reasoning_effort": settings.reasoning_effort,
        "openai_configured": settings.api_key_configured,
        "max_agents": settings.max_agents,
        "max_rounds": settings.max_rounds,
        "max_calls": settings.max_calls,
        "experimental": True,
    }


@app.get("/api/v1/agents", response_model=list[AgentPublic])
async def agents() -> list[AgentPublic]:
    return [AgentPublic(id=role.id, name=role.name, role=role.role, accent=role.accent) for role in ROLES]


@app.post("/api/v1/runs", status_code=status.HTTP_202_ACCEPTED)
async def create_run(payload: RunCreate) -> dict[str, str]:
    if not settings.api_key_configured:
        raise HTTPException(status_code=503, detail="The server requires OPENAI_API_KEY before live runs can start.")
    try:
        run_id = await orchestrator.create(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"run_id": run_id, "status": "queued", "events_url": f"/api/v1/runs/{run_id}/events"}


@app.get("/api/v1/runs")
async def list_runs(limit: int = 50):
    return await store.list_runs(min(max(limit, 1), 100))


@app.get("/api/v1/runs/{run_id}")
async def get_run(run_id: str):
    run = await store.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@app.post("/api/v1/runs/{run_id}/cancel", status_code=status.HTTP_202_ACCEPTED)
async def cancel_run(run_id: str):
    if not await orchestrator.cancel(run_id):
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run_id": run_id, "status": "cancellation_requested"}


@app.delete("/api/v1/runs/{run_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_run(run_id: str):
    run = await store.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    if run.status not in {"completed", "partial", "failed", "cancelled"}:
        raise HTTPException(status_code=409, detail="Active runs must be cancelled before deletion")
    await store.delete_run(run_id)
    return Response(status_code=204)


@app.get("/api/v1/runs/{run_id}/events")
async def events(run_id: str, request: Request, last_event_id: str | None = Header(default=None)):
    if not await store.get_run(run_id):
        raise HTTPException(status_code=404, detail="Run not found")
    try:
        after = max(int(last_event_id or request.query_params.get("after", "0")), 0)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Last-Event-ID must be a non-negative integer") from exc

    async def generate():
        async for event in hub.stream(run_id, after):
            if await request.is_disconnected():
                break
            if event is None:
                yield ": heartbeat\n\n"
                continue
            data = event.model_dump_json()
            yield f"id: {event.sequence}\nevent: {event.type}\ndata: {data}\n\n"

    return StreamingResponse(
        generate(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache, no-transform", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
    )


frontend_dist = Path(__file__).resolve().parents[1] / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    async def frontend(path: str):
        candidate = frontend_dist / path
        if path and candidate.is_file() and frontend_dist in candidate.resolve().parents:
            return FileResponse(candidate)
        return FileResponse(frontend_dist / "index.html")
