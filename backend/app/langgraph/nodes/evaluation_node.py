import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.core.logging_config import LogUtils

logger = logging.getLogger(__name__)


async def evaluation_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    LogUtils.entry(logger, "evaluation", query=state["query"])

    evaluation = await runtime.context.evaluation.evaluate_pipeline(
        question=state["query"],
        retrieval_results=state["retrieved_documents"],
        answer=state["answer"],
    )

    evaluation_ms = (time.perf_counter() - start) * 1000

    LogUtils.exit(logger, "evaluation", start, confidence=evaluation.retrieval.confidence.level)

    return {
        "evaluation": evaluation,
        "candidate_evaluations": [
                *state["candidate_evaluations"],
                evaluation,
            ],
        "evaluation_ms": evaluation_ms,
    }
