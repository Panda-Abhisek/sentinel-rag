import logging
import time

from app.rag.context_builder import ContextBuilder
from app.rag.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService
from app.core.logging_config import LogUtils

logger = logging.getLogger(__name__)

class GenerationService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    async def generate_answer(self, documents, question) -> str:

        start = time.perf_counter()
        LogUtils.entry(logger, "GenerationService.generate_answer", docs=len(documents))

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

        LogUtils.exit(logger, "GenerationService.generate_answer", start, answer_len=len(answer))
        return answer
