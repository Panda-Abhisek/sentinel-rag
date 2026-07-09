import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.core.logging_config import LogUtils
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames

logger = logging.getLogger(__name__)


async def planner_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()

    LogUtils.entry(
        logger,
        "planner",
        query=state["query"],
    )

    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        node_name=NodeNames.PLANNER,
        retry=state.get("retry_count", 0),
    ) as timer:

        decision = await runtime.context.planner.plan(
            state["query"]
        )

        timer.set_decision(
            decision=decision.planner_route,
            reason=decision.reason,
        )

    LogUtils.exit(
        logger,
        "planner",
        start,
        route=decision.planner_route,
    )

    return {
        "planner_route": decision.planner_route,
        "planner_reason": decision.reason,
    }