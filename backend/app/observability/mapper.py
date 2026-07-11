from app.observability.models import ExecutionSummary, NodeExecution, TokenUsage
from app.schemas.observability import (
    NodeExecutionResponse,
    ObservabilityResponse,
    TokenUsageResponse,
)


class ObservabilityMapper:

    @staticmethod
    def to_response(summary: ExecutionSummary) -> ObservabilityResponse:
        return ObservabilityResponse(
            request_id=summary.request_id,
            graph_path=summary.graph_path,
            total_latency_ms=summary.total_latency_ms,
            retries=summary.retries,
            final_confidence=summary.final_confidence,
            selected_attempt=summary.selected_attempt,
            token_usage=ObservabilityMapper._sum_token_usage(summary),
            nodes=[
                ObservabilityMapper._map_node(node)
                for node in summary.nodes
            ],
        )

    @staticmethod
    def _map_node(node: NodeExecution) -> NodeExecutionResponse:
        return NodeExecutionResponse(
            node_name=node.node_name,
            duration_ms=node.duration_ms,
            success=node.success,
            retry=node.retry,
            decision=node.decision,
            reason=ObservabilityMapper._truncate(node.reason),
            exception_type=node.exception_type,
            recovery_action=node.recovery_action,
            recovered=node.recovered,
        )

    @staticmethod
    def _truncate(text: str | None, max_length: int = 80) -> str | None:
        if text is None:
            return None
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."

    @staticmethod
    def _sum_token_usage(summary: ExecutionSummary) -> TokenUsageResponse:
        total = TokenUsage()
        for node in summary.nodes:
            total.prompt_tokens += node.token_usage.prompt_tokens
            total.completion_tokens += node.token_usage.completion_tokens
            total.total_tokens += node.token_usage.total_tokens
            total.estimated_cost += node.token_usage.estimated_cost
        return TokenUsageResponse(
            prompt_tokens=total.prompt_tokens,
            completion_tokens=total.completion_tokens,
            total_tokens=total.total_tokens,
            estimated_cost=total.estimated_cost,
        )
