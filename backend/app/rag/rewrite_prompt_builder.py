"""
Prompt builder for SentinelRAG query rewriting.

This module constructs prompts used by the query rewriting component.
Its sole responsibility is prompt construction. It does not perform
LLM inference or query rewriting itself.
"""

import inspect
import logging

logger = logging.getLogger(__name__)


class RewritePromptBuilder:
    """
    Builds prompts for rewriting user queries.

    The generated prompts instruct an LLM to improve retrieval quality
    while preserving the user's original intent.
    """

    _SYSTEM_PROMPT = inspect.cleandoc(
        """
        You are an expert search query optimizer for a
        Retrieval-Augmented Generation (RAG) system.

        Your task is to rewrite user queries to improve document
        retrieval while preserving the original intent.

        Rules:

        - Preserve the user's intent.
        - Do not answer the question.
        - Expand vague or underspecified queries.
        - Add useful context only when implied.
        - Improve clarity and specificity.
        - Keep the rewritten query concise.
        - Return only the rewritten query.
        - Do not include explanations, markdown, or quotation marks.
        """
    )

    _USER_TEMPLATE = inspect.cleandoc(
        """
        Original query:

        {query}

        Rewrite the query for optimal semantic retrieval.
        """
    )

    def __init__(self) -> None:
        """
        Initialize the rewrite prompt builder.
        """
        logger.info("RewritePromptBuilder initialized.")

    def build(
        self,
        query: str,
    ) -> list[dict[str, str]]:
        """
        Build the prompt for query rewriting.

        Parameters
        ----------
        query:
            Original user query.

        Returns
        -------
        list[dict[str, str]]
            Chat messages formatted for the LLM.
        """
        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        logger.debug(
            "Building rewrite prompt (query_length=%d).",
            len(query),
        )

        return [
            {
                "role": "system",
                "content": self._SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": self._USER_TEMPLATE.format(
                    query=query,
                ),
            },
        ]