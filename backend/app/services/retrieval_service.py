from app.vectorstore.qdrant_client import QdrantService
from app.schemas.retrieval import QueryResponse
from app.services.llm_service import LLMService
from langchain_core.documents import Document
from app.rag.source_mapper import SourceMapper
from app.rag.prompt_builder import PromptBuilder
from app.rag.context_builder import ContextBuilder
import logging
import time
from app.core.config import settings
from app.evaluation.evaluation_logger import EvaluationLogger
from app.evaluation.evaluation_service import EvaluationService
from app.evaluation.models import LatencyMetrics

logger = logging.getLogger(__name__)

class RetrievalService:

    def __init__(
        self,
        qdrant_service: QdrantService,
        llm_service: LLMService,
        evaluation_service: EvaluationService,
    ):
        self.qdrant_service = qdrant_service
        self.llm_service = llm_service
        self.evaluation_service = evaluation_service
    
    def _retrieve_documents(
        self,
        question: str,
        top_k: int,
    ) -> list[tuple[Document, float]]:
        """
        Retrieve the most relevant documents from Qdrant.
        """

        return self.qdrant_service.search(
            query=question,
            top_k=top_k,
        )    
    
    async def retrieve_answer(
        self,
        question: str,
        top_k: int = settings.DEFAULT_TOP_K,
    ) -> QueryResponse:
        """
        Executes the complete Retrieval-Augmented Generation pipeline.
        """

        request_start = time.perf_counter()

        logger.info("=" * 80)
        logger.info("Processing retrieval request")
        logger.info("Question: %s", question)
        logger.info("Top-K: %d", top_k)

        try:
            # -------------------------------------------------------------
            # Retrieve Documents
            # -------------------------------------------------------------
            retrieval_start = time.perf_counter()

            documents = self._retrieve_documents(
                question=question,
                top_k=top_k,
            )

            retrieval_time = (time.perf_counter() - retrieval_start) * 1000

            logger.info(
                "Retrieved %d documents in %.2f ms.",
                len(documents),
                retrieval_time,
            )

            if not documents:
                logger.warning("No relevant documents found.")

                return QueryResponse(
                    answer=(
                        "I couldn't find any relevant information "
                        "in the indexed documents."
                    ),
                    sources=[],
                    evaluation=None,
                    latency=LatencyMetrics(
                        retrieval_ms=retrieval_time,
                        generation_ms=llm_time,
                        evaluation_ms=evaluation_time,
                        total_ms=(time.perf_counter() - request_start) * 1000,
                    )
                )

            # -------------------------------------------------------------
            # Build Context
            # -------------------------------------------------------------
            context = ContextBuilder.build_context(documents)

            logger.info(
                "Context built successfully (%d characters).",
                len(context),
            )

            # -------------------------------------------------------------
            # Build Prompt
            # -------------------------------------------------------------
            prompt = PromptBuilder.build_qa_prompt(
                question=question,
                context=context,
            )

            logger.info(
                "Prompt constructed (%d characters).",
                len(prompt),
            )

            # -------------------------------------------------------------
            # Generate Answer
            # -------------------------------------------------------------
            llm_start = time.perf_counter()

            answer = await self.llm_service.generate(prompt)

            llm_time = (time.perf_counter() - llm_start) * 1000

            logger.info(
                "LLM generated response in %.2f ms.",
                llm_time,
            )

            logger.info(
                "Answer length: %d characters.",
                len(answer),
            )

            ## -------------------------------------------------------------
            # Evaluate
            # -------------------------------------------------------------
            evaluation = None
            evaluation_time = 0.0

            if settings.ENABLE_EVALUATION:
                try:
                    evaluation_start = time.perf_counter()

                    evaluation = await self.evaluation_service.evaluate_pipeline(
                        question=question,
                        retrieval_results=documents,
                        answer=answer,
                    )

                    evaluation_time = (
                        time.perf_counter() - evaluation_start
                    ) * 1000

                    logger.info(
                        "Evaluation completed in %.2f ms.",
                        evaluation_time,
                    )

                    EvaluationLogger.log(evaluation)
                except Exception:
                    logger.exception(
                        "Evaluation pipeline failed."
                    )

            # -------------------------------------------------------------
            # Map Sources
            # -------------------------------------------------------------
            sources = SourceMapper.source_mapper(documents)

            logger.info(
                "Mapped %d source documents.",
                len(sources),
            )

            # -------------------------------------------------------------
            # Total Latency
            # -------------------------------------------------------------
            total_time = (time.perf_counter() - request_start) * 1000

            logger.info(
                "Retrieval request completed successfully in %.2f ms.",
                total_time,
            )

            logger.info("=" * 80)

            return QueryResponse(
                answer=answer,
                sources=sources,
                evaluation=evaluation,
                latency=LatencyMetrics(
                    retrieval_ms=retrieval_time,
                    generation_ms=llm_time,
                    evaluation_ms=evaluation_time,
                    total_ms=total_time,
                )
            )

        except Exception:
            logger.exception("Retrieval pipeline failed.")
            raise