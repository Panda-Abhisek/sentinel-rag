import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames


async def evaluation_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()

    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        logger=runtime.context.tracing.logger,
        request_id=runtime.context.tracing.request_id,
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
            reason=f"faithfulness={evaluation.answer.faithfulness}, overall={evaluation.answer.overall_score}"
        )

    evaluation_ms = (time.perf_counter() - start) * 1000

    return {
        "evaluation": evaluation,
        "candidate_evaluations": [
                *state["candidate_evaluations"],
                evaluation,
            ],
        "evaluation_ms": evaluation_ms,
    }
