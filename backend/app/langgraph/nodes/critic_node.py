import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.state import SentinelState
from app.langgraph.dependencies import SentinelContext
from app.core.logging_config import LogUtils

logger = logging.getLogger(__name__)

async def critic_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    start = time.perf_counter()
    LogUtils.entry(logger, "critic", retry=state["retry_count"])

    if state["retry_count"] >= state["max_retries"]:
        LogUtils.exit(logger, "critic", start, decision="finish", reason="max_retries")
        return {
            "critic_route": "finish",
            "critic_reason": "Maximum retries reached.",
        }

    decision = await runtime.context.critic.review(
        question=state["query"],
        answer=state["answer"],
        evaluation=state["evaluation"],
    )

    LogUtils.exit(logger, "critic", start, decision=decision.critic_route)

    return {
        "critic_route": decision.critic_route,
        "critic_reason": decision.reason,
        "rewritten_query": decision.rewritten_query,
    }
