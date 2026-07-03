from app.langgraph.state import SentinelState


def critic_node(state: SentinelState) -> SentinelState:
    return state