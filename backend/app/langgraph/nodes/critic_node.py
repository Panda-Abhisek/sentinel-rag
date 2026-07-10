from langgraph.runtime import Runtime

from app.langgraph.state import SentinelState
from app.langgraph.dependencies import SentinelContext
from app.observability.timing import NodeTimer
from app.observability.constants import NodeNames

async def critic_node(
    state: SentinelState,
    runtime: Runtime[SentinelContext],
):

    manager = runtime.context.tracing.manager

    if state["retry_count"] >= state["max_retries"]:
        with NodeTimer(
            manager=manager,
            logger=runtime.context.tracing.logger,
            request_id=runtime.context.tracing.request_id,
            node_name=NodeNames.CRITIC,
            retry=state.get("retry_count", 0),
        ) as timer:
            timer.set_decision(
                decision="finish",
                reason="max_retries",
            )
        return {
            "critic_route": "finish",
            "critic_reason": "Maximum retries reached.",
        }

    with NodeTimer(
        manager=manager,
        logger=runtime.context.tracing.logger,
        request_id=runtime.context.tracing.request_id,
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

    return {
        "critic_route": critic_result.decision.critic_route,
        "critic_reason": critic_result.decision.reason,
        "rewritten_query": critic_result.decision.rewritten_query,
    }
