from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0
    model: str = ""
    
@dataclass
class NodeExecution:
    node_name: str
    started_at: datetime
    ended_at: datetime | None = None
    duration_ms: float = 0.0
    success: bool = True
    retry: int = 0
    decision: str | None = None
    reason: str | None = None
    error: str | None = None
    token_usage: TokenUsage = field(default_factory=TokenUsage)
    metadata: dict[str, Any] = field(default_factory=dict)
    
@dataclass
class ExecutionSummary:
    request_id: str
    graph_path: list[str] = field(default_factory=list)
    nodes: list[NodeExecution] = field(default_factory=list)

    total_latency_ms: float = 0.0
    retries: int = 0
    final_confidence: float = 0.0
    selected_attempt: int = 0