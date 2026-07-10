from typing import Optional

from app.observability import ExecutionSummaryManager
from app.observability.events import ObservabilityEvent
from app.observability.structured_logger import StructuredLogger

class NodeTimer:
    def __init__(
        self,
        manager: ExecutionSummaryManager,
        logger: StructuredLogger,
        request_id: str,
        node_name: str,
        retry: int = 0,
    ):
        self.manager = manager
        self.logger = logger
        self.request_id = request_id
        self.node_name = node_name
        self.retry = retry

        self.decision: Optional[str] = None
        self.reason: Optional[str] = None
        self._node = None

    def __enter__(self):
        self.manager.start_node(
            node_name=self.node_name,
            retry=self.retry,
        )
        self._node = self.manager.summary.nodes[-1]
        self.logger.emit(ObservabilityEvent(
            event="node_started",
            request_id=self.request_id,
            data={"node": self.node_name, "retry": self.retry},
        ))
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
            node_data = self._node.to_dict()
            node_data["error"] = str(exc_value)
            self.logger.emit(ObservabilityEvent(
                event="node_failed",
                request_id=self.request_id,
                level="ERROR",
                data=node_data,
            ))
            return False

        self.manager.finish_node(
            node_name=self.node_name,
            decision=self.decision,
            reason=self.reason,
        )
        self.logger.emit(ObservabilityEvent(
            event="node_finished",
            request_id=self.request_id,
            data={"node": self._node.to_dict()},
        ))

        return False