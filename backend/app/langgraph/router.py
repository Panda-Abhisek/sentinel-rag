import logging
from app.langgraph.state import SentinelState

logger = logging.getLogger(__name__)

def planner_router(state: SentinelState) -> str:
    """
    Placeholder router.

    Will later decide whether to:
    - retrieve
    - rewrite
    - multi-hop
    - finish
    """
    print("planner_route: ", state["planner_route"])
    return state["planner_route"]

def critic_router(state: SentinelState):
    return state["critic_route"]