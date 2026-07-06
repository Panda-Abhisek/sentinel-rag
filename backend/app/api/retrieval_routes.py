from fastapi import APIRouter, Depends
import logging

from app.api.dependencies import get_graph_service
from app.schemas.retrieval import QueryRequest, QueryResponse
from app.services.graph_service import GraphService

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
    graph_service: GraphService = Depends(
        get_graph_service,
    ),
):

    logger.info("Received query request.")

    return await graph_service.execute(
        question=request.question,
        top_k=request.top_k,
    )