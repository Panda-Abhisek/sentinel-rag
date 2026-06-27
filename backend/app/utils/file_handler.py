from pathlib import Path
from uuid import uuid4
import shutil
import os

from fastapi import UploadFile
from app.core.config import settings

#temp upload dir
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(file: UploadFile) -> str:
    """
    Saves an uploaded file to a temporary directory.
    
    Returns:
        Absolute path to the saved file.
    """
    
    unique_filename = f"{uuid4()}_{file.filename}"
    destination = UPLOAD_DIR / unique_filename
    
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return str(destination)


def delete_file(file_path: str) -> None:
    """Deletes a temporary uploaded file."""
    path = Path(file_path)
    
    if path.exists():
        os.remove(path)
    