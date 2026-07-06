import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.core.logging_config import LogUtils

logger = logging.getLogger(__name__)


async def retrieval_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    LogUtils.entry(logger, "retrieval", query=state["query"])

    docs = runtime.context.retrieval.retrieve_documents(
        question=state["query"],
        top_k=state["top_k"],
    )

    retrieval_ms = (time.perf_counter() - start) * 1000

    LogUtils.exit(logger, "retrieval", start, docs=len(docs))

    return {
        "retrieved_documents": docs,
        "retrieval_ms": retrieval_ms,
    }
