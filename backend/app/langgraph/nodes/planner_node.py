import logging
from app.langgraph.state import SentinelState
from app.langgraph.router import planner_router

logger = logging.getLogger(__name__)

def planner_node(state: SentinelState) -> SentinelState:
    
    query = state["query"].strip()
    
    if len(query.split()) > 12:
        return {
            "planner_route": "rewrite",
            "planner_reason": "Query is long and may benefit from rewriting."
        }
        
    return {
        "planner_route": "retrieve",
        "planner_reason": "Direct retrieval is sufficient."
    }