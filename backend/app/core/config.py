from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    
    PROJECT_NAME: str = "SentinelRAG"
    
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "sentinel_rag"
    QDRANT_URL: str = f"http://{QDRANT_HOST}:{QDRANT_PORT}"
    
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    LLM_MODEL: str = "qwen/qwen3-32b"
    
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()