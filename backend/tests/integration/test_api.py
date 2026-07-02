from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.healing.models import HealingReport, HealingResponse, SelectedAnswer
from tests.factories import query_response_factory
from app.api.dependencies import get_healing_service


@pytest.mark.asyncio
async def test_retrieval_called_twice(
    healing_service,
    retrieval_service,
    llm_service,
):
    """
    Healing should execute two retrievals.
    """

    original = query_response_factory(
        retrieval_confidence=0.30,
    )

    healed = query_response_factory()

    retrieval_service.retrieve_answer.side_effect = [
        original,
        healed,
    ]

    llm_service.generate.return_value = (
        "Improved query"
    )

    await healing_service.answer(
        "FastAPI"
    )

    assert (
        retrieval_service.retrieve_answer.await_count
        == 2
    )
    
    
    
@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def healing_service():
    return AsyncMock()



@pytest.fixture
def client(healing_service):

    app.dependency_overrides[get_healing_service] = (
        lambda: healing_service
    )

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()
    
def test_query_success(
    client,
    healing_service,
):
    """
    API should return a successful response.
    """

    response = query_response_factory()

    healing_service.answer.return_value = (
        HealingResponse(
            response=response,
            healing=HealingReport(
                original_query="FastAPI",
                healing_attempted=False,
                original_score=0.9,
                selected_answer=SelectedAnswer.ORIGINAL,
            ),
        )
    )

    result = client.post(
        "/query/",
        json={
            "question": "FastAPI"
        },
    )

    assert result.status_code == 200

    body = result.json()

    assert body["response"]["answer"]
    
    
    
def test_empty_question(client):
    """
    Empty requests should fail validation.
    """

    result = client.post(
        "/query/",
        json={
            "question": ""
        },
    )

    assert result.status_code == 422
    
    
def test_missing_question(client):
    """
    Missing required fields should return 422.
    """

    result = client.post(
        "/query/",
        json={},
    )

    assert result.status_code == 422
    
    
    
def test_internal_error(
    client,
    healing_service,
):
    """
    Internal failures should return HTTP 500.
    """

    healing_service.answer.side_effect = RuntimeError(
        "Unexpected failure"
    )

    result = client.post(
        "/query/",
        json={
            "question": "FastAPI"
        },
    )

    assert result.status_code == 500
    
    
    
def test_healing_metadata_returned(
    client,
    healing_service,
):
    """
    Healing metadata should be included in the API response.
    """

    response = query_response_factory()

    healing_service.answer.return_value = (
        HealingResponse(
            response=response,
            healing=HealingReport(
                original_query="FastAPI",
                rewritten_query="Explain FastAPI",
                healing_attempted=True,
                healing_success=True,
                retry_count=1,
                selected_answer=SelectedAnswer.HEALED,
                original_score=0.60,
                healed_score=0.92,
            ),
        )
    )

    result = client.post(
        "/query/",
        json={
            "question": "FastAPI"
        },
    )

    body = result.json()

    assert body["healing"]["healing_attempted"] is True

    assert body["healing"]["selected_answer"] == "healed"
    
    
    
def test_question_forwarded(
    client,
    healing_service,
):
    """
    The router should forward the user query unchanged.
    """

    response = query_response_factory()

    healing_service.answer.return_value = (
        HealingResponse(
            response=response,
            healing=HealingReport(
                original_query="FastAPI",
                healing_attempted=False,
                selected_answer=SelectedAnswer.ORIGINAL,
                original_score=0.9,
            ),
        )
    )

    client.post(
        "/query/",
        json={
            "question": "dependency injection"
        },
    )

    healing_service.answer.assert_awaited_once_with(
        "dependency injection"
    )
    
    
    
