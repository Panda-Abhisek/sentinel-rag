from dataclasses import asdict
from datetime import datetime, timezone

from app.observability.models import ExecutionSummary, NodeExecution, TokenUsage

class ExecutionSummaryManager:
    def __init__(self, request_id: str):
        self.summary = ExecutionSummary(request_id=request_id)

        # Keeps track of currently executing nodes
        self._active_nodes: dict[str, NodeExecution] = {}

    def to_dict(self) -> dict:
        return asdict(self)

    def start_node(self, node_name: str, retry: int = 0) -> None:
        """
        Start tracking execution of a graph node.
        """

        node = NodeExecution(
            node_name=node_name,
            started_at=datetime.now(timezone.utc),
            retry=retry,
        )

        self.summary.nodes.append(node)
        self.summary.graph_path.append(node_name)

        self._active_nodes[node_name] = node

    def finish_node(
        self,
        node_name: str,
        success: bool = True,
        decision: str | None = None,
        reason: str | None = None,
    ) -> None:
        """
        Finish execution of a node and calculate duration.
        """

        node = self._active_nodes.get(node_name)

        if node is None:
            return

        node.ended_at = datetime.now(timezone.utc)
        node.success = success
        node.decision = decision
        node.reason = reason

        node.duration_ms = (
            node.ended_at - node.started_at
        ).total_seconds() * 1000

        del self._active_nodes[node_name]

    def record_error(
        self,
        node_name: str,
        error: Exception,
    ) -> None:
        """
        Record an exception for a node.
        """

        node = self._active_nodes.get(node_name)

        if node is None:
            return

        node.success = False
        node.error = str(error)

        node.ended_at = datetime.now(timezone.utc)
        node.duration_ms = (
            node.ended_at - node.started_at
        ).total_seconds() * 1000

        del self._active_nodes[node_name]

    def add_token_usage(
        self,
        node_name: str,
        token_usage: TokenUsage,
    ) -> None:
        """
        Attach token usage information to a node.
        """

        for node in self.summary.nodes:
            if node.node_name == node_name:
                node.token_usage = token_usage
                return


    def complete(
        self,
        confidence: float,
        selected_attempt: int,
    ) -> ExecutionSummary:
        """
        Finalize the execution summary.
        """

        self.summary.final_confidence = confidence
        self.summary.selected_attempt = selected_attempt

        self.summary.total_latency_ms = sum(
            node.duration_ms for node in self.summary.nodes
        )

        self.summary.retries = max(
            (node.retry for node in self.summary.nodes),
            default=0,
        )

        return self.summary