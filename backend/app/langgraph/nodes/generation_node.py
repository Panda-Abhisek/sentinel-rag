import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.core.logging_config import LogUtils
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames

logger = logging.getLogger(__name__)


async def generation_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    LogUtils.entry(logger, "generation", query=state["query"])
    
    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
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

    LogUtils.exit(logger, "generation", start, answer_len=len(llm_response.answer))

    return {
        "answer": llm_response.answer,
        "candidate_answers":[
                *state["candidate_answers"],
                llm_response.answer
            ],
        "generation_ms": generation_ms,
    }
