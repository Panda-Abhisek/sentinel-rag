import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.core.logging_config import LogUtils
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames

logger = logging.getLogger(__name__)


async def evaluation_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    LogUtils.entry(logger, "evaluation", query=state["query"])

    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        node_name=NodeNames.EVALUATION,
        retry=state.get("retry_count", 0),
    ) as timer:

        evaluation = await runtime.context.evaluation.evaluate_pipeline(
            question=state["query"],
            retrieval_results=state["retrieved_documents"],
            answer=state["answer"],
        )

        timer.set_decision(
            decision="evaluation_complete",
            reason={evaluation.answer.faithfulness, evaluation.answer.overall_score}
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
