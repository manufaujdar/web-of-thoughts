from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable

from openai import AsyncOpenAI


DeltaCallback = Callable[[str], Awaitable[None]]


@dataclass(frozen=True)
class ProviderResult:
    text: str
    response_id: str | None
    input_tokens: int
    output_tokens: int


class OpenAIProvider:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(max_retries=2, timeout=90.0)

    async def generate(
        self, *, model: str, instructions: str, prompt: str, reasoning_effort: str,
        max_output_tokens: int, on_delta: DeltaCallback,
    ) -> ProviderResult:
        stream = await self.client.responses.create(
            model=model,
            instructions=instructions,
            input=prompt,
            reasoning={"effort": reasoning_effort},
            max_output_tokens=max_output_tokens,
            store=False,
            stream=True,
        )
        pieces: list[str] = []
        response_id: str | None = None
        input_tokens = 0
        output_tokens = 0
        async for event in stream:
            event_type = getattr(event, "type", "")
            if event_type == "response.output_text.delta":
                delta = getattr(event, "delta", "") or ""
                pieces.append(delta)
                await on_delta(delta)
            elif event_type == "response.completed":
                response = getattr(event, "response", None)
                response_id = getattr(response, "id", None)
                usage = getattr(response, "usage", None)
                input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
                output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
        text = "".join(pieces).strip()
        if not text:
            raise RuntimeError("model_returned_empty_output")
        return ProviderResult(text, response_id, input_tokens, output_tokens)
