from unittest.mock import AsyncMock, MagicMock

import pytest
from app.evaluation.evaluation_service import EvaluationService
from app.evaluation.models import AnswerEvaluation, HallucinationEvaluation
from tests.factories import retrieval_evaluation_factory
from langchain_core.documents import Document

@pytest.mark.asyncio
async def test_pipeline_continues_when_evaluation_fails(
    retrieval_service,
    qdrant_service,
    llm_service,
    evaluation_service,
):
    """
    Evaluation failures should not fail retrieval.
    """

    qdrant_service.search.return_value = [
        (
            Document(
                page_content="Dependency Injection",
                metadata={
                    "page": 1,
                    "source": "fastapi.pdf",
                },
            ),
            0.90,
        )
    ]

    llm_service.generate.return_value = (
        "Dependency Injection..."
    )

    evaluation_service.evaluate_pipeline.side_effect = (
        RuntimeError("Evaluation failed")
    )

    response = await retrieval_service.retrieve_answer(
        "Dependency Injection"
    )

    assert response.answer

    assert response.evaluation is None
    
    
@pytest.fixture
def retrieval_evaluator():
    return MagicMock()


@pytest.fixture
def answer_evaluator():
    return AsyncMock()


@pytest.fixture
def hallucination_detector():
    return AsyncMock()


@pytest.fixture
def evaluation_service(
    retrieval_evaluator,
    answer_evaluator,
    hallucination_detector,
):
    return EvaluationService(
        retrieval_evaluator=retrieval_evaluator,
        answer_evaluator=answer_evaluator,
        hallucination_detector=hallucination_detector,
    )
    
    
@pytest.fixture
def retrieval_results():

    return [
        (
            Document(
                page_content="Dependency Injection is a design pattern.",
                metadata={
                    "page": 1,
                    "source": "fastapi.pdf",
                },
            ),
            0.91,
        ),
        (
            Document(
                page_content="FastAPI uses dependency injection extensively.",
                metadata={
                    "page": 2,
                    "source": "fastapi.pdf",
                },
            ),
            0.88,
        ),
    ]
    
    
@pytest.mark.asyncio
async def test_complete_evaluation_pipeline(
    evaluation_service,
    retrieval_results,
    retrieval_evaluator,
    answer_evaluator,
    hallucination_detector,
):
    """
    Evaluation pipeline should combine all evaluation components.
    """

    retrieval_evaluator.evaluate.return_value = (
        retrieval_evaluation_factory()
    )

    answer_evaluator.evaluate.return_value = (
        AnswerEvaluation(
            faithfulness=0.90,
            answer_relevancy=0.92,
            context_utilization=0.88,
            completeness=0.91,
        )
    )

    hallucination_detector.evaluate.return_value = (
        HallucinationEvaluation(
            hallucination_score=0.05,
        )
    )

    report = await evaluation_service.evaluate_pipeline(
        question="What is DI?",
        retrieval_results=retrieval_results,
        answer="Dependency Injection is...",
    )

    assert report.retrieval is not None

    assert report.answer is not None

    assert report.hallucination is not None
    
    
@pytest.mark.asyncio
async def test_answer_evaluator_failure(
    evaluation_service,
    retrieval_results,
    retrieval_evaluator,
    answer_evaluator,
    hallucination_detector,
):
    """
    Exceptions raised by the answer evaluator should propagate.
    """

    retrieval_evaluator.evaluate.return_value = (
        retrieval_evaluation_factory()
    )

    hallucination_detector.evaluate.return_value = (
        HallucinationEvaluation(
            hallucination_score=0.10,
        )
    )

    answer_evaluator.evaluate.side_effect = RuntimeError(
        "Answer evaluation failed"
    )

    with pytest.raises(RuntimeError):

        await evaluation_service.evaluate_pipeline(
            question="Question",
            retrieval_results=retrieval_results,
            answer="Answer",
        )
        
        
@pytest.mark.asyncio
async def test_hallucination_detector_failure(
    evaluation_service,
    retrieval_results,
    retrieval_evaluator,
    answer_evaluator,
    hallucination_detector,
):
    """
    Exceptions raised by hallucination detection should propagate.
    """

    retrieval_evaluator.evaluate.return_value = (
        retrieval_evaluation_factory()
    )

    answer_evaluator.evaluate.return_value = (
        AnswerEvaluation(
            faithfulness=0.9,
            answer_relevancy=0.9,
            context_utilization=0.9,
            completeness=0.9,
        )
    )

    hallucination_detector.evaluate.side_effect = (
        RuntimeError("Detector failed")
    )

    with pytest.raises(RuntimeError):

        await evaluation_service.evaluate_pipeline(
            question="Question",
            retrieval_results=retrieval_results,
            answer="Answer",
        )
        
        
@pytest.mark.asyncio
async def test_parallel_evaluators_are_called(
    evaluation_service,
    retrieval_results,
    retrieval_evaluator,
    answer_evaluator,
    hallucination_detector,
):
    """
    Both asynchronous evaluators should be executed.
    """

    retrieval_evaluator.evaluate.return_value = (
        retrieval_evaluation_factory()
    )

    answer_evaluator.evaluate.return_value = (
        AnswerEvaluation(
            faithfulness=1.0,
            answer_relevancy=1.0,
            context_utilization=1.0,
            completeness=1.0,
        )
    )

    hallucination_detector.evaluate.return_value = (
        HallucinationEvaluation(
            hallucination_score=0.0,
        )
    )

    await evaluation_service.evaluate_pipeline(
        question="Question",
        retrieval_results=retrieval_results,
        answer="Answer",
    )

    answer_evaluator.evaluate.assert_awaited_once()

    hallucination_detector.evaluate.assert_awaited_once()
    
    
    
@pytest.mark.asyncio
async def test_retrieval_evaluator_called(
    evaluation_service,
    retrieval_results,
    retrieval_evaluator,
    answer_evaluator,
    hallucination_detector,
):
    """
    Retrieval evaluation should always execute exactly once.
    """

    retrieval_evaluator.evaluate.return_value = (
        retrieval_evaluation_factory()
    )

    answer_evaluator.evaluate.return_value = (
        AnswerEvaluation(
            faithfulness=0.9,
            answer_relevancy=0.9,
            context_utilization=0.9,
            completeness=0.9,
        )
    )

    hallucination_detector.evaluate.return_value = (
        HallucinationEvaluation(
            hallucination_score=0.1,
        )
    )

    await evaluation_service.evaluate_pipeline(
        question="Question",
        retrieval_results=retrieval_results,
        answer="Answer",
    )

    retrieval_evaluator.evaluate.assert_called_once()
    
    
    
