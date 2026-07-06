from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState


async def selector_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    index = runtime.context.selector.select(
        state["candidate_answers"],
        state["candidate_evaluations"],
    )

    return {
        "answer": state["candidate_answers"][index],
        "evaluation": state["candidate_evaluations"][index],
        "selected_answer_index": index,
    }