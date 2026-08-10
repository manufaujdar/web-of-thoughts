from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


RunStatus = Literal["queued", "running", "completed", "partial", "failed", "cancelled"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RunCreate(BaseModel):
    query: str = Field(min_length=3, max_length=12_000)
    agent_ids: list[str] | None = Field(default=None, max_length=8)
    rounds: int = Field(default=2, ge=1, le=2)
    max_calls: int = Field(default=20, ge=2, le=20)
    max_wall_seconds: int = Field(default=180, ge=30, le=300)

    @field_validator("query")
    @classmethod
    def normalize_query(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("query cannot be blank")
        return cleaned

    @field_validator("agent_ids")
    @classmethod
    def unique_agents(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return None
        if len(value) != len(set(value)):
            raise ValueError("agent_ids must be unique")
        return value


class AgentPublic(BaseModel):
    id: str
    name: str
    role: str
    accent: str


class RunEvent(BaseModel):
    sequence: int
    run_id: str
    type: str
    timestamp: str
    payload: dict[str, Any]


class RunSummary(BaseModel):
    id: str
    query: str
    status: RunStatus
    model: str
    created_at: str
    updated_at: str
    final_answer: str | None = None
    error: str | None = None
    snapshot: dict[str, Any]
