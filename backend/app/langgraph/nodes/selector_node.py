import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.core.logging_config import LogUtils

logger = logging.getLogger(__name__)


async def selector_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    LogUtils.entry(logger, "selector", candidates=len(state["candidate_answers"]))

    index = runtime.context.selector.select(
        state["candidate_answers"],
        state["candidate_evaluations"],
    )

    LogUtils.exit(logger, "selector", start, selected=index)

    return {
        "answer": state["candidate_answers"][index],
        "evaluation": state["candidate_evaluations"][index],
        "selected_answer_index": index,
    }
