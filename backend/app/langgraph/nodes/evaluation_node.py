import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState


async def evaluation_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()

    evaluation = await runtime.context.evaluation.evaluate_pipeline(
        question=state["query"],
        retrieval_results=state["retrieved_documents"],
        answer=state["answer"],
    )
    
    return {
        "evaluation": evaluation,
        "candidate_evaluations": [
                *state["candidate_evaluations"],
                evaluation,
            ],
        "evaluation_ms": (
            time.perf_counter() - start
        ) * 1000,
    }