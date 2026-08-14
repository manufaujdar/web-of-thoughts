from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str = "Web of Thoughts"
    model: str = "gpt-5.6-sol"
    reasoning_effort: str = "medium"
    database_path: Path = Path("data/wot.db")
    max_agents: int = 8
    max_rounds: int = 2
    max_concurrency: int = 4
    max_calls: int = 20
    max_wall_seconds: int = 300
    agent_output_tokens: int = 700
    master_output_tokens: int = 1600
    retention_days: int = 30
    allowed_origins: tuple[str, ...] = ("http://localhost:5173", "http://127.0.0.1:5173")

    @property
    def api_key_configured(self) -> bool:
        return bool(os.environ.get("OPENAI_API_KEY", "").strip())

    @classmethod
    def from_env(cls) -> "Settings":
        origins = tuple(
            item.strip()
            for item in os.environ.get(
                "WOT_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
            ).split(",")
            if item.strip()
        )
        return cls(
            model=os.environ.get("WOT_MODEL", "gpt-5.6-sol"),
            reasoning_effort=os.environ.get("WOT_REASONING_EFFORT", "medium"),
            database_path=Path(os.environ.get("WOT_DATABASE_PATH", "data/wot.db")),
            max_agents=int(os.environ.get("WOT_MAX_AGENTS", "8")),
            max_rounds=int(os.environ.get("WOT_MAX_ROUNDS", "2")),
            max_concurrency=int(os.environ.get("WOT_MAX_CONCURRENCY", "4")),
            max_calls=int(os.environ.get("WOT_MAX_CALLS", "20")),
            max_wall_seconds=int(os.environ.get("WOT_MAX_WALL_SECONDS", "300")),
            agent_output_tokens=int(os.environ.get("WOT_AGENT_OUTPUT_TOKENS", "700")),
            master_output_tokens=int(os.environ.get("WOT_MASTER_OUTPUT_TOKENS", "1600")),
            retention_days=int(os.environ.get("WOT_RETENTION_DAYS", "30")),
            allowed_origins=origins,
        )
