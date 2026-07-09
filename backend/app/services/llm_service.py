import logging
import time
import re
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from app.core.config import settings
from app.core.logging_config import LogUtils
from app.models.LLMResponse import LLMResponse
from app.observability.models import TokenUsage

logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.LLM_MODEL,
            temperature=settings.GENERATION_TEMPERATURE,
            max_tokens=settings.GENERATION_MAX_TOKENS,
        )

    async def generate(
        self,
        prompt: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:

        start = time.perf_counter()
        LogUtils.entry(logger, "LLMService.generate", model=settings.LLM_MODEL)

        llm = self.llm

        if temperature is not None or max_tokens is not None:
            llm = ChatGroq(
                api_key=settings.GROQ_API_KEY,
                model=settings.LLM_MODEL,
                temperature=(
                    temperature
                    if temperature is not None
                    else settings.GENERATION_TEMPERATURE
                ),
                max_tokens=(
                    max_tokens
                    if max_tokens is not None
                    else settings.GENERATION_MAX_TOKENS
                ),
            )

        try:
            response = await llm.ainvoke(
                [HumanMessage(content=prompt)]
            )

            answer = response.content
            
            logger.info("Response Metadata: %s", response.response_metadata)
            logger.info("Usage Metadata: %s", getattr(response, "usage_metadata", None))

            LogUtils.exit(logger, "LLMService.generate", start, answer_len=len(answer))

            return LLMResponse(
                content=answer,
                model=response.response_metadata["model_name"],
                usage=TokenUsage(
                    prompt_tokens=response.usage_metadata["input_tokens"],
                    completion_tokens=response.usage_metadata["output_tokens"],
                    total_tokens=response.usage_metadata["total_tokens"],
                    model=response.response_metadata["model_name"],
                ),
            )

        except Exception:
            logger.exception("LLM generation failed.")
            raise
