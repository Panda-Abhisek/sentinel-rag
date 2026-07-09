from typing import Optional

from app.observability import ExecutionSummaryManager

class NodeTimer:
    def __init__(
        self,
        manager: ExecutionSummaryManager,
        node_name: str,
        retry: int = 0,
    ):
        self.manager = manager
        self.node_name = node_name
        self.retry = retry

        self.decision: Optional[str] = None
        self.reason: Optional[str] = None

    def __enter__(self):
        self.manager.start_node(
            node_name=self.node_name,
            retry=self.retry,
        )
        return self

    def set_decision(
        self,
        decision: str,
        reason: str | None = None,
    ):
        self.decision = decision
        self.reason = reason

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is not None:
            self.manager.record_error(
                self.node_name,
                exc_value,
            )
            return False

        self.manager.finish_node(
            node_name=self.node_name,
            decision=self.decision,
            reason=self.reason,
        )

        return False