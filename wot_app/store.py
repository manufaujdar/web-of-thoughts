from __future__ import annotations

import asyncio
import json
import sqlite3
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .models import RunEvent, RunSummary, utc_now


class RunStore:
    def __init__(self, path: Path):
        self.path = path
        self._lock = asyncio.Lock()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=5000")
        return connection

    async def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        async with self._lock:
            await asyncio.to_thread(self._initialize_sync)

    def _initialize_sync(self) -> None:
        with closing(self._connect()) as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    query TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('queued','running','completed','partial','failed','cancelled')),
                    model TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    final_answer TEXT,
                    error TEXT,
                    snapshot_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS events (
                    run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
                    sequence INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    PRIMARY KEY(run_id, sequence)
                );
                CREATE INDEX IF NOT EXISTS idx_runs_created ON runs(created_at DESC);
                """
            )
            db.execute(
                "UPDATE runs SET status='failed', error='server_restarted', updated_at=? WHERE status IN ('queued','running')",
                (utc_now(),),
            )
            db.commit()

    async def create_run(self, run_id: str, query: str, model: str, snapshot: dict[str, Any]) -> None:
        now = utc_now()
        async with self._lock:
            await asyncio.to_thread(self._create_run_sync, run_id, query, model, snapshot, now)

    def _create_run_sync(self, run_id: str, query: str, model: str, snapshot: dict[str, Any], now: str) -> None:
        with closing(self._connect()) as db:
            db.execute(
                "INSERT INTO runs VALUES (?, ?, 'queued', ?, ?, ?, NULL, NULL, ?)",
                (run_id, query, model, now, now, json.dumps(snapshot)),
            )
            db.commit()

    async def update_run(
        self, run_id: str, *, status: str | None = None, snapshot: dict[str, Any] | None = None,
        final_answer: str | None = None, error: str | None = None,
    ) -> None:
        fields = ["updated_at=?"]
        values: list[Any] = [utc_now()]
        for name, value in (("status", status), ("snapshot_json", json.dumps(snapshot) if snapshot is not None else None), ("final_answer", final_answer), ("error", error)):
            if value is not None:
                fields.append(f"{name}=?")
                values.append(value)
        values.append(run_id)
        async with self._lock:
            await asyncio.to_thread(self._execute, f"UPDATE runs SET {', '.join(fields)} WHERE id=?", values)

    async def append_event(self, run_id: str, event_type: str, payload: dict[str, Any]) -> RunEvent:
        async with self._lock:
            return await asyncio.to_thread(self._append_event_sync, run_id, event_type, payload)

    def _append_event_sync(self, run_id: str, event_type: str, payload: dict[str, Any]) -> RunEvent:
        timestamp = utc_now()
        with closing(self._connect()) as db:
            row = db.execute("SELECT COALESCE(MAX(sequence), 0) + 1 AS seq FROM events WHERE run_id=?", (run_id,)).fetchone()
            sequence = int(row["seq"])
            db.execute(
                "INSERT INTO events VALUES (?, ?, ?, ?, ?)",
                (run_id, sequence, event_type, timestamp, json.dumps(payload)),
            )
            db.commit()
        return RunEvent(sequence=sequence, run_id=run_id, type=event_type, timestamp=timestamp, payload=payload)

    def _execute(self, statement: str, values: list[Any]) -> None:
        with closing(self._connect()) as db:
            db.execute(statement, values)
            db.commit()

    async def get_run(self, run_id: str) -> RunSummary | None:
        return await asyncio.to_thread(self._get_run_sync, run_id)

    def _get_run_sync(self, run_id: str) -> RunSummary | None:
        with closing(self._connect()) as db:
            row = db.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
        return self._row_to_run(row) if row else None

    async def list_runs(self, limit: int = 50) -> list[RunSummary]:
        return await asyncio.to_thread(self._list_runs_sync, limit)

    def _list_runs_sync(self, limit: int) -> list[RunSummary]:
        with closing(self._connect()) as db:
            rows = db.execute("SELECT * FROM runs ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [self._row_to_run(row) for row in rows]

    async def prune_terminal_runs(self, retention_days: int) -> int:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=max(retention_days, 1))).isoformat()
        async with self._lock:
            return await asyncio.to_thread(self._prune_terminal_runs_sync, cutoff)

    def _prune_terminal_runs_sync(self, cutoff: str) -> int:
        with closing(self._connect()) as db:
            cursor = db.execute(
                "DELETE FROM runs WHERE status IN ('completed','partial','failed','cancelled') AND updated_at < ?",
                (cutoff,),
            )
            db.commit()
            return cursor.rowcount

    async def delete_run(self, run_id: str) -> bool:
        async with self._lock:
            return await asyncio.to_thread(self._delete_run_sync, run_id)

    def _delete_run_sync(self, run_id: str) -> bool:
        with closing(self._connect()) as db:
            cursor = db.execute(
                "DELETE FROM runs WHERE id=? AND status IN ('completed','partial','failed','cancelled')", (run_id,)
            )
            db.commit()
            return cursor.rowcount == 1

    async def events_after(self, run_id: str, after: int = 0) -> list[RunEvent]:
        return await asyncio.to_thread(self._events_after_sync, run_id, after)

    def _events_after_sync(self, run_id: str, after: int) -> list[RunEvent]:
        with closing(self._connect()) as db:
            rows = db.execute(
                "SELECT * FROM events WHERE run_id=? AND sequence>? ORDER BY sequence", (run_id, after)
            ).fetchall()
        return [RunEvent(sequence=row["sequence"], run_id=run_id, type=row["event_type"], timestamp=row["timestamp"], payload=json.loads(row["payload_json"])) for row in rows]

    @staticmethod
    def _row_to_run(row: sqlite3.Row) -> RunSummary:
        return RunSummary(
            id=row["id"], query=row["query"], status=row["status"], model=row["model"],
            created_at=row["created_at"], updated_at=row["updated_at"],
            final_answer=row["final_answer"], error=row["error"], snapshot=json.loads(row["snapshot_json"]),
        )
