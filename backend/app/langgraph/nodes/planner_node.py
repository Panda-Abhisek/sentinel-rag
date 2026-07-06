import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.core.logging_config import LogUtils

logger = logging.getLogger(__name__)


async def planner_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    LogUtils.entry(logger, "planner", query=state["query"])

    decision = await runtime.context.planner.plan(
        state["query"]
    )

    LogUtils.exit(logger, "planner", start, route=decision.planner_route)

    return {
        "planner_route": decision.planner_route,
        "planner_reason": decision.reason,
    }
