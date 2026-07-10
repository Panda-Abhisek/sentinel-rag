import json
import logging
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any


class StructuredLogger:
    """
    Emits structured JSON logs for SentinelRAG observability.

    This class is responsible only for formatting and emitting logs.
    It does not calculate timings or collect metrics.
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def _log(
        self,
        level: int,
        event: str,
        **fields: Any,
    ) -> None:

        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            **fields,
        }

        self.logger.log(
            level,
            json.dumps(payload, default=str),
        )

    # ---------------------------------------------------------
    # Node Events
    # ---------------------------------------------------------

    def node_started(
        self,
        request_id: str,
        node_name: str,
        retry: int,
    ) -> None:

        self._log(
            logging.INFO,
            event="node_started",
            request_id=request_id,
            node=node_name,
            retry=retry,
        )

    def node_finished(
        self,
        request_id: str,
        node_execution,
    ) -> None:

        self._log(
            logging.INFO,
            event="node_finished",
            request_id=request_id,
            node=asdict(node_execution),
        )

    def node_failed(
        self,
        request_id: str,
        node_execution,
    ) -> None:

        self._log(
            logging.ERROR,
            event="node_failed",
            request_id=request_id,
            node=asdict(node_execution),
        )

    # ---------------------------------------------------------
    # Graph Events
    # ---------------------------------------------------------

    def graph_started(
        self,
        request_id: str,
        query: str,
    ) -> None:

        self._log(
            logging.INFO,
            event="graph_started",
            request_id=request_id,
            query=query,
        )

    def graph_finished(
        self,
        execution_summary,
    ) -> None:

        self._log(
            logging.INFO,
            event="graph_finished",
            summary=asdict(execution_summary),
        )

    # ---------------------------------------------------------
    # Generic
    # ---------------------------------------------------------

    def info(
        self,
        event: str,
        **fields,
    ) -> None:

        self._log(
            logging.INFO,
            event,
            **fields,
        )

    def warning(
        self,
        event: str,
        **fields,
    ) -> None:

        self._log(
            logging.WARNING,
            event,
            **fields,
        )

    def error(
        self,
        event: str,
        **fields,
    ) -> None:

        self._log(
            logging.ERROR,
            event,
            **fields,
        )