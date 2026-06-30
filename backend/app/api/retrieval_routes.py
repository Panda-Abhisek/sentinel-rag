from fastapi import APIRouter, Depends
import logging

from app.api.dependencies import get_retrieval_service
from app.schemas.retrieval import QueryRequest, QueryResponse
from app.services.retrieval_service import RetrievalService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/query",
    tags=["Query"],
)


@router.post(
    "/",
    response_model=QueryResponse,
)
async def query(
    request: QueryRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
) -> QueryResponse:
    """
    Query the RAG system.
    """

    logger.info("Received query request.")

    return await retrieval_service.retrieve_answer(
        question=request.question,
        top_k=request.top_k,
    )