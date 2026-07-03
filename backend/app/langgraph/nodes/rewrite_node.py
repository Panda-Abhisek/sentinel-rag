from app.langgraph.state import SentinelState


def rewrite_node(state: SentinelState) -> SentinelState:
    return state