"""
Integration tests for the RetrievalService pipeline.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from langchain_core.documents import Document

from app.services.retrieval_service import RetrievalService
from tests.factories import evaluation_report_factory


@pytest.fixture
def qdrant_service():
    return MagicMock()


@pytest.fixture
def llm_service():
    return AsyncMock()


@pytest.fixture
def evaluation_service():
    return AsyncMock()


@pytest.fixture
def retrieval_service(
    qdrant_service,
    llm_service,
    evaluation_service,
):
    return RetrievalService(
        qdrant_service=qdrant_service,
        llm_service=llm_service,
        evaluation_service=evaluation_service,
    )
    
    
@pytest.mark.asyncio
async def test_retrieval_pipeline_success(
    retrieval_service,
    qdrant_service,
    llm_service,
    evaluation_service,
):
    """
    Complete retrieval pipeline should produce a valid response.
    """

    documents = [
        (
            Document(
                page_content="Dependency Injection is a design pattern.",
                metadata={
                    "page": 1,
                    "source": "fastapi.pdf",
                },
            ),
            0.92,
        )
    ]

    qdrant_service.search.return_value = documents

    llm_service.generate.return_value = (
        "Dependency Injection is a technique..."
    )

    evaluation_service.evaluate_pipeline.return_value = (
        evaluation_report_factory()
    )

    response = await retrieval_service.retrieve_answer(
        "What is Dependency Injection?"
    )

    assert response.answer

    assert len(response.sources) == 1

    assert response.evaluation is not None

    assert response.latency.total_ms > 0
    

@pytest.mark.asyncio
async def test_no_documents_found(
    retrieval_service,
    qdrant_service,
):
    """
    Retrieval should gracefully handle an empty vector search.
    """

    qdrant_service.search.return_value = []

    response = await retrieval_service.retrieve_answer(
        "Unknown question"
    )

    assert response.sources == []

    assert "couldn't find" in response.answer.lower()
    
    
    
@pytest.mark.asyncio
async def test_pipeline_without_evaluation(
    monkeypatch,
    retrieval_service,
    qdrant_service,
    llm_service,
):
    """
    Pipeline should still succeed when evaluation is disabled.
    """

    from app.core.config import settings

    monkeypatch.setattr(
        settings,
        "ENABLE_EVALUATION",
        False,
    )

    qdrant_service.search.return_value = [
        (
            Document(
                page_content="FastAPI",
                metadata={
                    "page": 1,
                    "source": "test.pdf",
                },
            ),
            0.90,
        )
    ]

    llm_service.generate.return_value = "FastAPI"

    response = await retrieval_service.retrieve_answer(
        "FastAPI"
    )

    assert response.evaluation is None
    
    
    
@pytest.mark.asyncio
async def test_generation_failure(
    retrieval_service,
    qdrant_service,
    llm_service,
):
    """
    Retrieval pipeline should propagate LLM failures.
    """

    qdrant_service.search.return_value = [
        (
            Document(
                page_content="FastAPI",
                metadata={
                    "page": 1,
                    "source": "test.pdf",
                },
            ),
            0.90,
        )
    ]

    llm_service.generate.side_effect = RuntimeError(
        "Groq unavailable"
    )

    with pytest.raises(RuntimeError):
        await retrieval_service.retrieve_answer(
            "FastAPI"
        )
        
        
        
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
    
    
    
