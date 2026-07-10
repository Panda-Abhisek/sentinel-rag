from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class ObservabilityEvent:
    """
    Base event emitted by the observability system.
    """

    event: str

    request_id: str

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)