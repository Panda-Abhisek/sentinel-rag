"""
Retry strategy for SentinelRAG.

This module contains the RetryStrategy responsible for preparing a
retrieval retry after the healing policy determines that a second
attempt should be made.

The strategy currently rewrites the original user query while
preserving its intent. It does not execute retrieval or answer
generation. Those responsibilities belong to the HealingService.
"""

import logging

from app.healing.query_rewriter import QueryRewriter

logger = logging.getLogger(__name__)


class RetryStrategy:
    """
    Prepare a retry request for the self-healing pipeline.

    The retry strategy validates the original query and produces an
    improved query that can be used by the retrieval pipeline during a
    healing attempt.
    """

    def __init__(
        self,
        query_rewriter: QueryRewriter,
    ) -> None:
        self.query_rewriter = query_rewriter

        logger.info("RetryStrategy initialized.")

    async def retry(
        self,
        query: str,
    ) -> str:
        """
        Prepare a rewritten query for a retrieval retry.

        Parameters
        ----------
        query:
            Original user query.

        Returns
        -------
        str
            Rewritten query suitable for retrying retrieval.
        """

        self._validate_query(query)

        logger.info(
            "Starting retry strategy for query rewrite."
        )

        rewritten_query = await self._rewrite_query(query)

        logger.info(
            "Retry strategy completed successfully."
        )

        return rewritten_query

    async def _rewrite_query(
        self,
        query: str,
    ) -> str:
        """
        Rewrite the original query for a retrieval retry.
        """

        logger.debug("Rewriting query.")

        rewritten_query = await self.query_rewriter.rewrite(query)

        logger.debug("Query rewritten successfully.")

        return rewritten_query

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