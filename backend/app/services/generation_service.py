import logging
import time

from app.rag.context_builder import ContextBuilder
from app.rag.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class GenerationService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    async def generate_answer(self, documents, question) -> str:
        
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
        return answer
