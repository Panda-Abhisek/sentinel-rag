from app.langgraph.state import SentinelState


def reflection_node(state: SentinelState) -> SentinelState:
    return state