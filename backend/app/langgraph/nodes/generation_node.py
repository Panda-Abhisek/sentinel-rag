import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState


async def generation_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()

    answer = await runtime.context.generation.generate_answer(
        question=state["query"],
        documents=state["retrieved_documents"],
    )
    
    return {
        "answer": answer,
        "candidate_answers":[
                *state["candidate_answers"],
                answer
            ],
        "generation_ms": (
            time.perf_counter() - start
        ) * 1000,
    }