"""
Self-healing orchestration service for SentinelRAG.

This module contains the HealingService, the central orchestrator
responsible for executing SentinelRAG's self-healing retrieval
workflow.

The service coordinates retrieval, evaluation, retry decision-making,
query rewriting, answer comparison, and healing report generation. It
delegates all domain-specific logic to specialized services while
remaining responsible only for workflow orchestration.

Pipeline

User Query
    │
    ▼
Initial Retrieval
    │
    ▼
Evaluation
    │
    ▼
Healing Policy
    │
 ┌──┴───┐
 │      │
No     Yes
 │      │
 ▼      ▼
Return  Retry Strategy
          │
          ▼
    Query Rewrite
          │
          ▼
    Retrieval Retry
          │
          ▼
    Answer Selector
          │
          ▼
    Healing Report
          │
          ▼
    HealingResponse
"""

import time
import logging

from app.healing.answer_selector import AnswerSelector
from app.healing.healing_policy import HealingPolicy
from app.healing.retry_strategy import RetryStrategy
from app.healing.models import HealingReport, HealingResponse, SelectedAnswer
from app.services.retrieval_service import RetrievalService

logger = logging.getLogger(__name__)

class HealingService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        healing_policy: HealingPolicy,
        retry_strategy: RetryStrategy,
        answer_selector: AnswerSelector,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.healing_policy = healing_policy
        self.retry_strategy = retry_strategy
        self.answer_selector = answer_selector
        logger.info("HealingService initialized.")  
        
        
    async def answer(
        self,
        query: str,
    ) -> HealingResponse:
        """
        Execute the complete self-healing retrieval workflow.

        The workflow performs an initial retrieval and evaluation. If the
        healing policy determines that the response quality is insufficient,
        the query is rewritten and the retrieval pipeline is executed again.
        The original and healed responses are then compared, and the better
        answer is returned together with a detailed healing report.

        Parameters
        ----------
        query:
            User query.

        Returns
        -------
        HealingResponse
            Final response selected by the healing pipeline together with its
            healing metadata.
        """
        start = time.perf_counter()
        query = query.strip()
        self._validate_query(query)
        logger.info(
            "Starting self-healing pipeline."
        )
        original_answer = await self.retrieval_service.retrieve_answer(query)
        logger.info(
            "Original retrieval completed (score=%.3f).",
            original_answer.evaluation.answer.overall_score,
        )
        decision = self.healing_policy.decide(original_answer.evaluation)
        logger.info(
            "Healing decision: retry=%s reason=%s",
            decision.should_retry,
            decision.retry_reason,
        )
        
        if not decision.should_retry:
            logger.info(
                "Healing not required. Returning original response."
            )
            return HealingResponse(
                response=original_answer, 
                healing=HealingReport(
                    original_query=query,
                    healing_attempted=False,
                    healing_success=False,
                    retry_count=0,
                    retry_reason=None,
                    selected_answer=SelectedAnswer.ORIGINAL,
                    original_score=original_answer.evaluation.answer.overall_score,
                    latency_overhead_ms=(time.perf_counter() - start) * 1000,
                )   
            )
        
        try:
            logger.info(
                "Executing healing retry (reason=%s).",
                decision.retry_reason.value,
            )
            rewritten_query = await self.retry_strategy.retry(query)
            logger.info(
                "Query rewritten successfully."
            )
            healed_answer = await self.retrieval_service.retrieve_answer(rewritten_query)
            logger.info(
                "Retry retrieval completed."
            )
            
            selection = self.answer_selector.select(original_answer, healed_answer)
            winner = selection.response
            
            logger.info(
                "Answer selection completed."
            )
        except Exception:
            logger.exception(
                "Healing pipeline failed. Returning original response."
            )

            healing_report = self._build_failed_healing_report(
                original_query=query,
                decision=decision,
                original_answer=original_answer,
                latency_ms=(time.perf_counter() - start) * 1000,
            )

            return HealingResponse(
                response=original_answer,
                healing=healing_report,
            )
            
        latency = (
            time.perf_counter() - start
        ) * 1000
        
        healing_report = self._build_healing_report(
            original_query=query,
            rewritten_query=rewritten_query,
            decision=decision,
            selected_answer=selection.selected_answer,
            winner_reason=selection.winner_reason,
            original_answer=original_answer,
            healed_answer=healed_answer,
            latency_ms=latency,
        )
        
        logger.info(
            "Self-healing pipeline completed.",
        )
        return HealingResponse(
            response=winner,
            healing=healing_report
        )
        
    def _build_healing_report(
        self,
        *,
        original_query: str,
        rewritten_query: str,
        decision,
        selected_answer,
        winner_reason,
        original_answer,
        healed_answer,
        latency_ms: float,
    ) -> HealingReport:
        """
        Build a healing report for a successful healing workflow.

        Parameters
        ----------
        original_query:
            Original user query.

        rewritten_query:
            Query produced by the retry strategy.

        decision:
            Healing decision generated by the HealingPolicy.

        selected:
            Final answer selected by the AnswerSelector.

        original_answer:
            Original retrieval response.

        healed_answer:
            Response generated after the retry.

        latency_ms:
            Total healing pipeline latency in milliseconds.

        Returns
        -------
        HealingReport
            Report describing the completed healing workflow.
        """

        return HealingReport(
            original_query=original_query,
            rewritten_query=rewritten_query,
            healing_attempted=True,
            healing_success=True,
            retry_count=1,
            retry_reason=decision.retry_reason,
            selected_answer=selected_answer,
            winner_reason=winner_reason,
            original_score=original_answer.evaluation.answer.overall_score,
            healed_score=healed_answer.evaluation.answer.overall_score,
            latency_overhead_ms=latency_ms,
        )


    def _build_failed_healing_report(
        self,
        *,
        original_query: str,
        decision,
        original_answer,
        latency_ms: float,
    ) -> HealingReport:
        """
        Build a healing report when the retry workflow fails.

        Parameters
        ----------
        original_query:
            Original user query.

        decision:
            Healing decision generated by the HealingPolicy.

        original_answer:
            Response from the initial retrieval.

        latency_ms:
            Total elapsed time before the failure occurred.

        Returns
        -------
        HealingReport
            Report describing the failed healing attempt.
        """

        return HealingReport(
            original_query=original_query,
            healing_attempted=True,
            healing_success=False,
            retry_count=1,
            retry_reason=decision.retry_reason,
            selected_answer=SelectedAnswer.ORIGINAL,
            original_score=original_answer.evaluation.answer.overall_score,
            healed_score=None,
            latency_overhead_ms=latency_ms,
        )
        
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

        if not query:
            raise ValueError("Query cannot be empty.")