from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from app.observability.execution_summary import ExecutionSummaryManager


@dataclass
class TracingContext:
    request_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    manager: ExecutionSummaryManager = field(init=False)

    def __post_init__(self):
        self.manager = ExecutionSummaryManager(
            request_id=self.request_id
        )