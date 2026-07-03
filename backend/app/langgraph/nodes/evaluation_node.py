from app.langgraph.state import SentinelState


def evaluation_node(state: SentinelState) -> SentinelState:
    return state