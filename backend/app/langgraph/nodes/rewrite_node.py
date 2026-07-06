from langgraph.runtime import Runtime

from app.langgraph.state import SentinelState
from app.langgraph.dependencies import SentinelContext


async def rewrite_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    rewritten_query = await runtime.context.rewriter.rewrite(
        question=state["query"],
        answer=state["answer"],
        evaluation=state["evaluation"],
    )

    return {
        "rewritten_query": rewritten_query,
        "query": rewritten_query or state["query"],
        "retry_count": state["retry_count"] + 1,
    }