"""
Query rewriting service for SentinelRAG.

This module provides the QueryRewriter responsible for improving user
queries before retrieval when the self-healing pipeline determines a
retry is necessary.

The service validates the input query, constructs a rewrite prompt,
invokes the configured language model, and returns a rewritten query
while preserving the original user intent.

If rewriting fails for any reason, the original query is returned so
that the retrieval pipeline can continue without interruption.
"""

import logging

from app.rag.rewrite_prompt_builder import RewritePromptBuilder
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class QueryRewriter:
    """
    Service responsible for rewriting user queries to improve retrieval.

    The rewriter delegates prompt construction to the
    RewritePromptBuilder and text generation to the LLMService.
    """

    def __init__(
        self,
        llm_service: LLMService,
        prompt_builder: RewritePromptBuilder,
    ) -> None:
        self.llm_service = llm_service
        self.prompt_builder = prompt_builder

        logger.info("QueryRewriter initialized.")

    async def rewrite(
        self,
        query: str,
    ) -> str:
        """
        Rewrite a user query while preserving its original intent.

        Parameters
        ----------
        query:
            Original user query.

        Returns
        -------
        str
            Rewritten query. If rewriting fails, the original query is
            returned.
        """

        self._validate_query(query)

        logger.info("Starting query rewrite.")

        try:
            prompt = self.prompt_builder.build(query)

            rewritten_query = await self.llm_service.generate(
                prompt,
                temperature=0.2,
                max_tokens=128,
            )

            rewritten_query = self._clean_response(rewritten_query)

            logger.info(
                "Query successfully rewritten "
                "(original_length=%d, rewritten_length=%d).",
                len(query),
                len(rewritten_query),
            )

            return rewritten_query

        except Exception:
            logger.exception(
                "Query rewriting failed. Falling back to original query."
            )
            return query

    def _validate_query(
        self,
        query: str,
    ) -> None:
        """
        Validate the input query.

        Raises
        ------
        ValueError
            If the query is empty or contains only whitespace.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

    def _clean_response(
        self,
        rewritten_query: str,
    ) -> str:
        """
        Clean the rewritten query returned by the language model.

        Parameters
        ----------
        rewritten_query:
            Raw model output.

        Returns
        -------
        str
            Normalized rewritten query.
        """

        cleaned = rewritten_query.strip()

        if not cleaned:
            logger.warning(
                "LLM returned an empty rewritten query. "
                "Using original output."
            )
            return rewritten_query.strip()

        return cleaned