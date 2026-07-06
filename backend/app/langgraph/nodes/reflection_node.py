from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState


async def reflection_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    report = await runtime.context.reflection.reflect(
        selected_index=state["selected_answer_index"],
        answers=state["candidate_answers"],
        evaluations=state["candidate_evaluations"],
    )

    return {
        "reflection": report,
    }