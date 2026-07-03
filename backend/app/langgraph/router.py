from app.langgraph.state import SentinelState


def route(state: SentinelState) -> str:
    """
    Placeholder router.

    Will later decide whether to:
    - retrieve
    - rewrite
    - multi-hop
    - finish
    """
    return "retrieve"