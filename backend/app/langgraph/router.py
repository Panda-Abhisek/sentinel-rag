import logging
from app.langgraph.state import SentinelState

logger = logging.getLogger(__name__)

def planner_router(state: SentinelState) -> str:
    route = state["planner_route"]
    logger.info("Planner routing to: %s", route)
    return route

def critic_router(state: SentinelState):
    route = state["critic_route"]
    logger.info("Critic routing to: %s", route)
    return route
