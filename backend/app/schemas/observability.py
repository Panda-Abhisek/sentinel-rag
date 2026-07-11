from pydantic import BaseModel


class TokenUsageResponse(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float


class NodeExecutionResponse(BaseModel):
    node_name: str
    duration_ms: float
    success: bool
    retry: int
    decision: str | None
    reason: str | None
    exception_type: str | None
    recovery_action: str | None
    recovered: bool


class ObservabilityResponse(BaseModel):
    request_id: str
    graph_path: list[str]
    total_latency_ms: float
    retries: int
    final_confidence: float
    selected_attempt: int
    token_usage: TokenUsageResponse
    nodes: list[NodeExecutionResponse]
