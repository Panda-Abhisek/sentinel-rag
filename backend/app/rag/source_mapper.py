# app/rag/source_mapper.py

from langchain_core.documents import Document

from app.schemas.retrieval import SourceDocument


class SourceMapper:
    """
    Maps retrieved LangChain documents into API response models.

    Responsibilities:
    - Convert retrieved documents into SourceDocument schemas.
    - Extract relevant metadata.
    - Preserve similarity scores for transparency.

    Future responsibilities:
    - Include chunk IDs.
    - Include document IDs.
    - Support richer metadata for citations.
    """

    @staticmethod
    def source_mapper(
        documents: list[tuple[Document, float]],
    ) -> list[SourceDocument]:
        """
        Convert retrieved documents into SourceDocument objects.

        Args:
            documents:
                Retrieved LangChain documents paired with similarity scores.

        Returns:
            A list of SourceDocument objects returned to the client.
        """

        return [
            SourceDocument(
                source=document.metadata.get("source", "Unknown"),
                page=document.metadata.get("page", 0),
                score=score,
                content=document.page_content,
            )
            for document, score in documents
        ]