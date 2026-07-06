import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.core.logging_config import LogUtils

logger = logging.getLogger(__name__)


async def generation_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    LogUtils.entry(logger, "generation", query=state["query"])

    answer = await runtime.context.generation.generate_answer(
        question=state["query"],
        documents=state["retrieved_documents"],
    )

    generation_ms = (time.perf_counter() - start) * 1000

    LogUtils.exit(logger, "generation", start, answer_len=len(answer))

    return {
        "answer": answer,
        "candidate_answers":[
                *state["candidate_answers"],
                answer
            ],
        "generation_ms": generation_ms,
    }
