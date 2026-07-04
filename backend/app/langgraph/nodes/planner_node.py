from app.langgraph.state import SentinelState


def planner_node(state: SentinelState) -> SentinelState:
    query = state["query"].strip()
    
    if len(query.split()) > 12:
        return {
            "route": "rewrite",
            "planner_reason": "Query is long and may benefit from rewriting."
        }
        
    return {
        "route": "retrieve",
        "planner_reason": "Direct retrieval is sufficient."
    }