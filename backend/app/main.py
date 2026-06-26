import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResult
from services.index_service import IndexService

app = FastAPI(
    title = "SentinelRAG",
    version = "1.0.0"
)

TEMP_DIR = Path("/tmp/rag_uploads")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

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
    
    
@app.post("/documents/upload")
async def upload_and_index_documents(file: UploadFile = File(...)):
    #1. Validate that the received file is a PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    temp_file_path = TEMP_DIR / file.filename
    
    try:
        #2 Save incoming file stream temporarily to disk
        with temp_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        #3 Offload execution to your isloated Index Service
        _, chunk_count = IndexService.process_and_index_pdf(
            file_path=str(temp_file_path),
            collection_name="document_collection"
        )
        
        #4 Construct response payload on pipeline completion
        return {
            "status": "success",
            "filename": file.filename,
            "chunks": chunk_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")
    
    finally:
        if temp_file_path.exists():
            os.remove(temp_file_path)
            print(f"Safely purged temp cache for file: {file.filename}")
            
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)