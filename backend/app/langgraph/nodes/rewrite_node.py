import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.state import SentinelState
from app.langgraph.dependencies import SentinelContext
from app.core.logging_config import LogUtils
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames

logger = logging.getLogger(__name__)


async def rewrite_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    LogUtils.entry(logger, "rewrite", query=state["query"])

    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        node_name=NodeNames.REWRITE,
        retry=state.get("retry_count", 0),
    ) as timer:

        rewritten_query = await runtime.context.rewriter.rewrite(
            question=state["query"],
            answer=state["answer"],
            evaluation=state["evaluation"],
        )

        timer.set_decision(
            decision="rewrite_complete",
            reason=f"Query rewritten: {rewritten_query}",
        )

    LogUtils.exit(logger, "rewrite", start, rewritten=bool(rewritten_query))

    return {
        "rewritten_query": rewritten_query,
        "query": rewritten_query or state["query"],
        "retry_count": state["retry_count"] + 1,
    }
