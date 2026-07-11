from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames


async def reflection_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        logger=runtime.context.tracing.logger,
        request_id=runtime.context.tracing.request_id,
        node_name=NodeNames.REFLECTION,
        retry=state.get("retry_count", 0),
    ) as timer:

        reflection_result = await runtime.context.reflection.reflect(
            selected_index=state["selected_answer_index"],
            answers=state["candidate_answers"],
            evaluations=state["candidate_evaluations"],
        )
        
        manager.add_token_usage(
            "reflection",
            reflection_result.token_usage,
        )

        timer.set_decision(
            decision="reflection_complete",
            reason=f"Reflection generated: {reflection_result.result.selected_attempt}",
        )

    return {
        "reflection": reflection_result.result,
    }
