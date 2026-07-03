from langgraph.graph import StateGraph, START, END

from app.langgraph.state import SentinelState


builder = StateGraph(SentinelState)

builder.add_edge(START, END)

graph = builder.compile()