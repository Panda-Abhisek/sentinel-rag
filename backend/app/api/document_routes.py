from pathlib import Path
import logging
from fastapi import UploadFile, File, HTTPException, status, APIRouter
from app.utils.file_handler import save_uploaded_file, delete_file
from app.schemas.index import IndexResult
from app.services.index_service import IndexService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

# post /documents/upload
@router.post("/upload", response_model=IndexResult, status_code=status.HTTP_201_CREATED,)
async def upload_document(file: UploadFile = File(...)) -> IndexResult:
    """Uploads a PDF document, indexes it into Qdrant, and returns indexing statistics."""
    
    #validate file extension
    if Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported."
        )
    
    temp_file_path = None
    
    try:
        # save uploaded file
        temp_file_path = save_uploaded_file(file)
        logger.info("File saved successfully: %s", temp_file_path)
        
        # run ingestion pipeline
        result = IndexService.process_and_index_pdf(file_path=temp_file_path, original_filename=file.filename)
        logger.info("Document indexed successfully.")
        return result
    except Exception as e:
        logger.exception("Document upload failed.")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    finally:
        if temp_file_path:
            delete_file(temp_file_path)


# get /documents
# delete /documents/{id}

