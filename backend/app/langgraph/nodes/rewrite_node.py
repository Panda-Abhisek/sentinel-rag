from app.langgraph.state import SentinelState

async def rewrite_node(
    state: SentinelState,
):
    return {
        "query": state["query"],
    }