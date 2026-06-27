from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

@router.get("/")
def health():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "SentinelRAG",
        "version": "1.0.0"
    }