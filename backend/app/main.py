from fastapi import FastAPI

from app.api.document_routes import router as document_router
from app.api.health_routes import router as health_router
from app.core.logging_config import setup_logging, add_correlation_middleware
from app.api.retrieval_routes import router as retrieval_router

setup_logging()

app = FastAPI(
    title = "SentinelRAG",
    version = "1.0.0"
)

add_correlation_middleware(app)

app.include_router(document_router)
app.include_router(health_router)
app.include_router(retrieval_router)

@app.get("/")
def home():
    return {
        "message": "SentinelRAG API Running"
    }
