from dataclasses import dataclass
from typing import Any

from app.observability.models import TokenUsage


@dataclass
class LLMResponse:
    content: str
    model: str
    usage: TokenUsage
    raw_response: Any | None = None