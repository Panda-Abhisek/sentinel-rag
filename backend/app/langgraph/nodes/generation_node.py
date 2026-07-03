from app.langgraph.state import SentinelState


def generation_node(state: SentinelState) -> SentinelState:
    return state