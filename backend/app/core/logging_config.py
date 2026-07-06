import logging
import time
import uuid
from contextvars import ContextVar

from fastapi import FastAPI, Request

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(correlation_id)s | %(message)s"

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="-")


class CorrelationFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = correlation_id_var.get()
        return True


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        force=True,
    )

    for handler in logging.getLogger().handlers:
        handler.addFilter(CorrelationFilter())

    noisy_loggers = (
        "httpx",
        "huggingface_hub",
        "sentence_transformers",
    )

    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


class LogUtils:

    @staticmethod
    def entry(logger: logging.Logger, node: str, **kwargs):
        extras = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        logger.info("Entering %s | %s", node, extras)

    @staticmethod
    def exit(logger: logging.Logger, node: str, start: float, **kwargs):
        duration_ms = (time.perf_counter() - start) * 1000
        extras = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        logger.info(
            "Exiting %s | duration_ms=%.2f | %s",
            node,
            duration_ms,
            extras,
        )


def add_correlation_middleware(app: FastAPI) -> None:
    logger = logging.getLogger("api")

    @app.middleware("http")
    async def correlation_middleware(request: Request, call_next):
        cid = request.headers.get(
            "X-Correlation-ID",
            uuid.uuid4().hex[:8],
        )
        correlation_id_var.set(cid)
        start = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "method=%s | path=%s | status=%d | duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        response.headers["X-Correlation-ID"] = cid
        return response
