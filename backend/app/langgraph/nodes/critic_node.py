import logging
import time

from langgraph.runtime import Runtime

from app.langgraph.state import SentinelState
from app.langgraph.dependencies import SentinelContext
from app.core.logging_config import LogUtils
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames

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

    manager = runtime.context.tracing.manager

    with NodeTimer(
        manager=manager,
        node_name=NodeNames.CRITIC,
        retry=state.get("retry_count", 0),
    ) as timer:

        critic_result = await runtime.context.critic.review(
            question=state["query"],
            answer=state["answer"],
            evaluation=state["evaluation"],
        )
        
        manager.add_token_usage(
            "critic",
            critic_result.token_usage,
        )
        
        timer.set_decision(
            decision=critic_result.decision.critic_route,
            reason=critic_result.decision.reason,
        )

    LogUtils.exit(logger, "critic", start, decision=critic_result.decision.critic_route)

    return {
        "critic_route": critic_result.decision.critic_route,
        "critic_reason": critic_result.decision.reason,
        "rewritten_query": critic_result.decision.rewritten_query,
    }
