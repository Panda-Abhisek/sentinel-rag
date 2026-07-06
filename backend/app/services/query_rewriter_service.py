import logging
import time

from app.core.logging_config import LogUtils

logger = logging.getLogger(__name__)


class QueryRewriterService:

    def __init__(self, llm_service):
        self.llm = llm_service

    async def rewrite(
        self,
        question: str,
        answer: str | None = None,
        evaluation=None,
    ) -> str:

        start = time.perf_counter()
        LogUtils.entry(logger, "QueryRewriterService.rewrite")

        if answer is None or evaluation is None:

            prompt = f"""
                Rewrite this search query to improve semantic retrieval.

                Question:
                {question}

                Return ONLY the rewritten query.
                """

        else:

            prompt = f"""
                You are an expert search query optimizer for an enterprise Retrieval-Augmented Generation (RAG) system.

                The previous retrieval did not produce an ideal answer.

                Your job is to rewrite the user's question so that another semantic search is more likely to retrieve better documents.

                Original Question:
                {question}

                Previous Answer:
                {answer}

                Evaluation:
                {evaluation.model_dump_json(indent=2)}

                Rules:

                - Preserve the user's intent.
                - Make the query more specific.
                - Add important missing concepts if needed.
                - Do not answer the question.
                - Return ONLY the rewritten query.
                """

        rewritten_query = await self.llm.generate(prompt)

        rewritten_query = rewritten_query.strip().strip('"')

        if not rewritten_query:
            logger.warning("Rewriter returned an empty query. Using original query.")
            LogUtils.exit(logger, "QueryRewriterService.rewrite", start, rewritten=False)
            return question

        LogUtils.exit(logger, "QueryRewriterService.rewrite", start, rewritten=True)
        return rewritten_query
