import logging

from langgraph.runtime import Runtime

from app.langgraph.state import SentinelState
from app.langgraph.dependencies import SentinelContext

logger = logging.getLogger(__name__)

async def critic_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    if state["retry_count"] >= state["max_retries"]:
        return {
            "critic_route": "finish",
            "critic_reason": "Maximum retries reached.",
        }

    decision = await runtime.context.critic.review(
        question=state["query"],
        answer=state["answer"],
        evaluation=state["evaluation"],
    )

    return {
        "critic_route": decision.critic_route,
        "critic_reason": decision.reason,
        "rewritten_query": decision.rewritten_query,
    }