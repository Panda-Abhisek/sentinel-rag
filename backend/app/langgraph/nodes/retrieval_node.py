import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState


async def retrieval_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()

    docs = runtime.context.retrieval.retrieve_documents(
        question=state["query"],
        top_k=state["top_k"],
    )
    
    return {
        "retrieved_documents": docs,
        "retrieval_ms": (
            time.perf_counter() - start
        ) * 1000,
    }

    # state["retrieved_documents"] = docs

    # state["retrieval_ms"] = (
    #     time.perf_counter() - start
    # ) * 1000

    # return state