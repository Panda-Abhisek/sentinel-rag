import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.core.logging_config import LogUtils
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames

logger = logging.getLogger(__name__)


async def reflection_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    LogUtils.entry(logger, "reflection", selected=state["selected_answer_index"])
    
    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        node_name=NodeNames.REFLECTION,
        retry=state.get("retry_count", 0),
    ) as timer:

        report = await runtime.context.reflection.reflect(
            selected_index=state["selected_answer_index"],
            answers=state["candidate_answers"],
            evaluations=state["candidate_evaluations"],
        )

        timer.set_decision(
            decision="reflection_complete",
            reason=f"Reflection generated: {report.selected_attempt}",
        )

    LogUtils.exit(logger, "reflection", start, confidence=report.confidence)

    return {
        "reflection": report,
    }
