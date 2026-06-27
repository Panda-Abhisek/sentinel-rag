# app/rag/context_builder.py

from langchain_core.documents import Document


class ContextBuilder:
    """
    Builds the context passed to the LLM from retrieved documents.

    Responsibilities:
    - Format retrieved chunks
    - Preserve source ordering
    - Prepare context for prompt generation

    Future responsibilities:
    - Deduplicate chunks
    - Apply similarity threshold
    - Limit context size
    - Token budgeting
    - Context compression
    """

    @staticmethod
    def build_context(
        documents: list[tuple[Document, float]],
    ) -> str:
        """
        Build a formatted context string from retrieved documents.

        Args:
            documents: Retrieved documents with similarity scores.

        Returns:
            Formatted context string.
        """

        context_parts = []

        for index, (document, score) in enumerate(documents, start=1):
            context_parts.append(
                "\n".join(
                    [
                        f"========== Source {index} ==========",
                        f"Page: {document.metadata.get('page', 'Unknown')}",
                        f"Score: {score:.3f}",
                        "",
                        document.page_content.strip(),
                    ]
                )
            )

        return "\n\n".join(context_parts)