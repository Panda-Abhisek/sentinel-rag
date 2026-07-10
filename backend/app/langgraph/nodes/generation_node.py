import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames

logger = logging.getLogger(__name__)


async def generation_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    
    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        logger=runtime.context.tracing.logger,
        request_id=runtime.context.tracing.request_id,
        node_name=NodeNames.GENERATION,
        retry=state.get("retry_count", 0),
    ) as timer:

        llm_response = await runtime.context.generation.generate_answer(
            question=state["query"],
            documents=state["retrieved_documents"]
        )
        
        manager.add_token_usage(
            "generation",
            llm_response.token_usage,
        )

        timer.set_decision(
            decision="generation_complete",
            reason=f"Answer generated successfully.",
        )

    generation_ms = (time.perf_counter() - start) * 1000

    return {
        "answer": llm_response.answer,
        "candidate_answers":[
                *state["candidate_answers"],
                llm_response.answer
            ],
        "generation_ms": generation_ms,
    }
