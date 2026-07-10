from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames


async def planner_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        logger=runtime.context.tracing.logger,
        request_id=runtime.context.tracing.request_id,
        node_name=NodeNames.PLANNER,
        retry=state.get("retry_count", 0),
    ) as timer:

        decision = await runtime.context.planner.plan(
            state["query"]
        )
        
        manager.add_token_usage(
            "planner",
            decision.token_usage,
        )

        timer.set_decision(
            decision=decision.decision.planner_route,
            reason=decision.decision.reason,
        )

    return {
        "planner_route": decision.decision.planner_route,
        "planner_reason": decision.decision.reason,
    }
