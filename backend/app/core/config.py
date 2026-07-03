from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SentinelRAG"

    GROQ_API_KEY: Optional[str] = None
    GROQ_TEMPERATURE: float = 1.0

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "sentinel_rag"

    EMBEDDING_MODEL: str = "BAAI/bge-base-en-v1.5"
    EMBEDDING_DEVICE: str = "cpu"

    
    DEFAULT_TOP_K: int = 4
    RETRIEVAL_THRESHOLD: float = 0.45
    MAX_CONTEXT_DOCUMENTS: int = 4
    MAX_CONTEXT_CHARS: int = 8000
    LLM_TEMPERATURE: float = 0.2
    
    NVIDIA_API_KEY: str
    # Generation
    # GENERATION_MODEL: str = "meta/llama-3.3-70b-instruct"
    LLM_MODEL: str = "qwen/qwen3-32b"
    GENERATION_MAX_TOKENS: int = 2048
    GENERATION_TEMPERATURE: float = 0.2

    # Evaluation
    EVALUATION_MODEL: str = "nvidia/nemotron-mini-4b-instruct"
    EVALUATION_MAX_TOKENS: int = 256
    EVALUATION_TEMPERATURE: float = 0.0

    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    DEBUG: bool = True

    UPLOAD_DIR: str = "temp_uploads"
    
    # Evaluation
    ENABLE_EVALUATION: bool = True
    
    EVALUATION_MAX_CONTEXT_LENGTH: int = 500
    EVALUATION_MAX_RETRIEVAL_RESULTS: int = 3

    EVALUATION_SCORE_HIGH: float = 0.85
    EVALUATION_SCORE_MEDIUM: float = 0.65

    @property
    def QDRANT_URL(self) -> str:
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()