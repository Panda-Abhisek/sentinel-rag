import logging
import time

from app.rag.context_builder import ContextBuilder
from app.rag.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService
from app.services.models import GenerationResult

logger = logging.getLogger(__name__)

class GenerationService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    async def generate_answer(self, documents, question) -> GenerationResult:

        start = time.perf_counter()
        logger.info("Entering GenerationService.generate_answer | docs=%d", len(documents))

        context = ContextBuilder.build_context(documents)

        logger.info(
            "Context built (%d characters).",
            len(context),
        )

        prompt = PromptBuilder.build_qa_prompt(
            question=question,
            context=context,
        )

        logger.info(
            "Prompt constructed (%d characters).",
            len(prompt),
        )

        answer = await self.llm_service.generate(prompt)
        logger.info("Exiting GenerationService.generate_answer | duration_ms=%.2f | answer_len=%d", (time.perf_counter() - start) * 1000, len(answer.content))
        return GenerationResult(
            answer=answer.content,
            token_usage=answer.usage
        )
