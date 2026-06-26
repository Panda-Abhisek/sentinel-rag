from fastapi import FastAPI

app = FastAPI(
    title = "SentinelRAG",
    version = "1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "SentinelRAG API Running"
    }
    
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }