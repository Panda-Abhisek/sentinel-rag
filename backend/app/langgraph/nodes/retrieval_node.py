import logging

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames

logger = logging.getLogger(__name__)


async def retrieval_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        logger=runtime.context.tracing.logger,
        request_id=runtime.context.tracing.request_id,
        node_name=NodeNames.RETRIEVAL,
        retry=state.get("retry_count", 0),
    ) as timer:

        documents =  runtime.context.retrieval.retrieve_documents(
            question=state["query"], top_k=state["top_k"]
        )

        timer.set_decision(
            decision="retrieval_complete",
            reason=f"Retrieved {len(documents)} documents",
        )

    return {
        "retrieved_documents": documents,
        "retrieval_ms": state["retrieval_ms"],
    }
