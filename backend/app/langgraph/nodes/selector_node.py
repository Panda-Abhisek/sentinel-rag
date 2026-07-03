from app.langgraph.state import SentinelState


def selector_node(state: SentinelState) -> SentinelState:
    return state