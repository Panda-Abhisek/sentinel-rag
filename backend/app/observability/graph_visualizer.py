from pathlib import Path


class GraphVisualizer:

    @staticmethod
    def save_mermaid(graph, output_path: str) -> None:
        """
        Save the compiled LangGraph as Mermaid markdown.
        """

        mermaid = graph.get_graph().draw_mermaid()

        mermaid = mermaid.replace(
            "classDef default fill:#f2f0ff,line-height:1.2",
            "classDef default fill:#f2f0ff,line-height:1.2,fill-opacity:0",
        )

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            f"```mermaid\n{mermaid}\n```",
            encoding="utf-8",
        )

    @staticmethod
    def save_png(graph, output_path: str) -> None:
        """
        Save the compiled LangGraph as a PNG image.
        """

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        png_bytes = graph.get_graph().draw_png()
        path.write_bytes(png_bytes)