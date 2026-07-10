import json
import logging

from app.observability.events import ObservabilityEvent


class StructuredLogger:

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def emit(
        self,
        event: ObservabilityEvent,
        level: int = logging.INFO,
    ) -> None:

        self.logger.log(
            level,
            json.dumps(
                event.to_dict(),
                default=str,
            ),
        )