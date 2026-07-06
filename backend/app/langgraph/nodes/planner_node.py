import logging

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState

logger = logging.getLogger(__name__)


async def planner_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    decision = await runtime.context.planner.plan(
        state["query"]
    )

    logger.info(
        "Planner selected route: %s",
        decision.planner_route,
    )

    return {
        "planner_route": decision.planner_route,
        "planner_reason": decision.reason,
    }