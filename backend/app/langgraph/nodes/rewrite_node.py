from langgraph.runtime import Runtime

from app.langgraph.state import SentinelState
from app.langgraph.dependencies import SentinelContext
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames


async def rewrite_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        logger=runtime.context.tracing.logger,
        request_id=runtime.context.tracing.request_id,
        node_name=NodeNames.REWRITE,
        retry=state.get("retry_count", 0),
    ) as timer:

        result = await runtime.context.rewriter.rewrite(
            question=state["query"],
            answer=state["answer"],
            evaluation=state["evaluation"],
        )
        
        manager.add_token_usage(
            "rewrite",
            result.token_usage,
        )

        timer.set_decision(
            decision="rewrite_complete",
            reason=f"Query rewritten: {result.rewritten_query}",
        )

    return {
        "rewritten_query": result.rewritten_query,
        "query": result.rewritten_query or state["query"],
        "retry_count": state["retry_count"] + 1,
    }
