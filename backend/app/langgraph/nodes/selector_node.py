import logging

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames

logger = logging.getLogger(__name__)


async def selector_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        logger=runtime.context.tracing.logger,
        request_id=runtime.context.tracing.request_id,
        node_name=NodeNames.SELECTOR,
        retry=state.get("retry_count", 0),
    ) as timer:

        index = runtime.context.selector.select(
            state["candidate_answers"],
            state["candidate_evaluations"],
        )

        timer.set_decision(
            decision="selection_complete",
            reason=f"Selected attempt index: {index}",
        )

    return {
        "answer": state["candidate_answers"][index],
        "evaluation": state["candidate_evaluations"][index],
        "selected_answer_index": index,
    }
