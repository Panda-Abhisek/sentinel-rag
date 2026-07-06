import json
import logging

logger = logging.getLogger(__name__)


class QueryRewriterService:

    def __init__(self, llm_service):
        self.llm = llm_service

    async def rewrite(
        self,
        question: str,
        answer: str,
        evaluation,
    ) -> str:

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

        logger.info("Rewriting query.")

        rewritten_query = await self.llm.generate(prompt)

        rewritten_query = rewritten_query.strip().strip('"')

        logger.info(
            "Rewritten query: %s",
            rewritten_query,
        )

        return rewritten_query