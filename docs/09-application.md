# Real-time multi-agent application

The repository includes a functional single-node research application. It uses real OpenAI Responses API calls; there is no production fallback that returns canned agent text.

## Runtime topology

1. The user submits a query and selects at least two server-defined specialists.
2. Specialists independently produce concise public decision artifacts in parallel.
3. In two-pass mode, each specialist receives the artifacts of its two graph neighbors and revises its position.
4. The controller records `derived_from`, `supports`, `refines`, and `synthesizes` relationships.
5. The master evaluates every final specialist artifact, resolves or scopes conflicts, and streams the final response.

Agents cannot recursively create agents, modify their system prompts, obtain arbitrary tools, or override budgets. Their interconnection is mediated by a deterministic topology and typed artifacts—not unbounded role-play chat.

## Local setup

Requirements: Python 3.11+, Node.js 20+, and an OpenAI API key with access to the configured model.

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY. Do not commit it.

python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'

cd frontend
npm install
npm run build
cd ..

set -a && source .env && set +a
wot-server
```

Open `http://127.0.0.1:8000`. For frontend development, run `npm run dev` in `frontend/`; Vite proxies API requests to the backend.

Docker is also supported:

```bash
docker compose up --build
```

## Live API

- `GET /api/v1/config` — safe runtime capabilities; never returns secrets
- `GET /api/v1/agents` — public role descriptions
- `POST /api/v1/runs` — validate and queue a live run
- `GET /api/v1/runs` and `GET /api/v1/runs/{id}` — persisted run snapshots
- `GET /api/v1/runs/{id}/events` — ordered, replayable server-sent events
- `POST /api/v1/runs/{id}/cancel` — request cancellation
- `GET /health/live` and `GET /health/ready` — process/configuration health

SSE events are persisted before publication and include monotonic IDs. Client disconnection does not cancel a paid run; reconnecting replays missed events. Explicit cancellation prevents later phases and marks the run honestly.

## Persistence and privacy

SQLite runs in WAL mode and is appropriate for one application process. User queries, public agent artifacts, final answers, model identifiers, response IDs in events, and usage counts are stored locally in `data/wot.db`. SQLite is not encrypted by default. Prompts and artifacts leave the device when sent to OpenAI.

The service does not store API keys, authorization headers, private hidden reasoning, or raw provider response bodies. Delete the database file only when the server is stopped if complete local erasure is required.

## Production boundary

Before internet exposure, add deployment-specific authentication, user ownership, rate/cost controls, encrypted storage, retention jobs, audit logging, reverse-proxy limits, monitoring, and a distributed event/store architecture if using multiple workers. The bundled server intentionally uses one worker because its live event hub is process-local.

## Real-provider smoke test

With `OPENAI_API_KEY` configured:

```bash
python3 tools/live_smoke.py
```

This launches a real three-call run (two specialists plus master), waits for a terminal state, and verifies non-empty persisted output and actual token usage. It incurs API cost. Without a key it exits as **not run**, never as a passing fake test.
