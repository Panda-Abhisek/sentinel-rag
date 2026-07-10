from app.langgraph.graph import graph
from app.observability.graph_visualizer import GraphVisualizer

GraphVisualizer.save_mermaid(
    graph,
    "docs/graph.md",
)

GraphVisualizer.save_png(
    graph,
    "docs/graph.png",
)

print("Graph exported successfully.")