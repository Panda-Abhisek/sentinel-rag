import os
from pathlib import Path
from typing import Callable

from dotenv import load_dotenv
from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from app.core.config import settings

LANGSMITH_ENABLED = settings.LANGSMITH_TRACING or (
    os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
)


def is_tracing_enabled() -> bool:
    """
    Returns whether LangSmith tracing is enabled.
    """
    return LANGSMITH_ENABLED


def trace_graph(name: str, get_metadata: Callable[..., dict] | None = None):
    """
    Decorator used to trace the entire graph execution.

    If tracing is disabled, returns the original function.
    Optionally accepts a get_metadata callable that receives the
    decorated function's arguments and returns a dict of metadata
    to attach to the LangSmith run.
    """

    def decorator(func):
        if not LANGSMITH_ENABLED:
            return func

        @traceable(name=name)
        async def wrapper(*args, **kwargs):
            if get_metadata:
                meta = get_metadata(*args, **kwargs)
                run_tree = get_current_run_tree()
                if run_tree:
                    run_tree.extra.setdefault("metadata", {}).update(meta)
            return await func(*args, **kwargs)

        return wrapper

    return decorator