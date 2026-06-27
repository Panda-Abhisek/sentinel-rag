from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SentinelRAG"

    GROQ_API_KEY: Optional[str] = None
    GROQ_TEMPERATURE: float = 1.0

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "sentinel_rag"

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DEVICE: str = "cpu"

    LLM_MODEL: str = "qwen/qwen3-32b"
    DEFAULT_TOP_K: int = 4
    RETRIEVAL_THRESHOLD: float = 0.45
    MAX_CONTEXT_DOCUMENTS: int = 4
    MAX_CONTEXT_CHARS: int = 8000
    LLM_TEMPERATURE: float = 0.2

    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    DEBUG: bool = True

    UPLOAD_DIR: str = "temp_uploads"

    @property
    def QDRANT_URL(self) -> str:
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()