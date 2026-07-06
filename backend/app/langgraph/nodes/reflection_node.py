import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.core.logging_config import LogUtils

logger = logging.getLogger(__name__)


async def reflection_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    LogUtils.entry(logger, "reflection", selected=state["selected_answer_index"])

    report = await runtime.context.reflection.reflect(
        selected_index=state["selected_answer_index"],
        answers=state["candidate_answers"],
        evaluations=state["candidate_evaluations"],
    )

    LogUtils.exit(logger, "reflection", start, confidence=report.confidence)

    return {
        "reflection": report,
    }
