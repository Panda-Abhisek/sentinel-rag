import os

from langsmith import traceable


LANGSMITH_ENABLED = (
    os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
)


def is_tracing_enabled() -> bool:
    """
    Returns whether LangSmith tracing is enabled.
    """
    return LANGSMITH_ENABLED


def trace_graph(name: str):
    """
    Decorator used to trace the entire graph execution.

    If tracing is disabled, returns the original function.
    """

    def decorator(func):
        if not LANGSMITH_ENABLED:
            return func

        return traceable(name=name)(func)

    return decorator