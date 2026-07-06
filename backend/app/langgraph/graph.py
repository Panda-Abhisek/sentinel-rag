from langgraph.graph import START, END, StateGraph

from app.langgraph.state import SentinelState

from app.langgraph.nodes.retrieval_node import retrieval_node
from app.langgraph.nodes.generation_node import generation_node
from app.langgraph.nodes.evaluation_node import evaluation_node
from app.langgraph.dependencies import SentinelContext
from app.langgraph.nodes.planner_node import planner_node
from app.langgraph.nodes.rewrite_node import rewrite_node
from app.langgraph.router import planner_router
from app.langgraph.nodes.critic_node import critic_node
from app.langgraph.router import critic_router


builder = StateGraph(state_schema=SentinelState, context_schema=SentinelContext)

builder.add_node("planner", planner_node)
builder.add_node("rewrite", rewrite_node)
builder.add_node("retrieve", retrieval_node)
builder.add_node("generate", generation_node)
builder.add_node("evaluate", evaluation_node)
builder.add_node("critic", critic_node)

builder.add_edge(START, "planner")
builder.add_conditional_edges(
    "planner",
    planner_router,
    {
        "retrieve": "retrieve",
        "rewrite": "rewrite",
    }
)
builder.add_edge("rewrite", "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", "evaluate")
builder.add_edge("evaluate", "critic")
builder.add_conditional_edges(
    "critic",
    critic_router,
    {
        "finish": END,
        "rewrite": "rewrite"
    }
)

graph = builder.compile()