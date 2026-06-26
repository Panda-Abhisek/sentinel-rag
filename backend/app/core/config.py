from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "sentinel_rag"
    
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    LLM_MODEL: str = "qwen/qwen3-32b"
    
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()