from langgraph.graph import START, END, StateGraph

from app.langgraph.state import SentinelState

from app.langgraph.nodes.retrieval_node import retrieval_node
from app.langgraph.nodes.generation_node import generation_node
from app.langgraph.nodes.evaluation_node import evaluation_node
from app.langgraph.dependencies import SentinelContext


builder = StateGraph(state_schema=SentinelState, context_schema=SentinelContext)

builder.add_node("retrieve", retrieval_node)
builder.add_node("generate", generation_node)
builder.add_node("evaluate", evaluation_node)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", "evaluate")
builder.add_edge("evaluate", END)

graph = builder.compile()