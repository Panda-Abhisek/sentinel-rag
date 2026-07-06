import logging
from pathlib import Path
from uuid import uuid4
import shutil
import os

from fastapi import UploadFile
from app.core.config import settings

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(file: UploadFile) -> str:

    unique_filename = f"{uuid4()}_{file.filename}"
    destination = UPLOAD_DIR / unique_filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.info("Saved uploaded file: %s", destination)
    return str(destination)


def delete_file(file_path: str) -> None:
    path = Path(file_path)

    if path.exists():
        os.remove(path)
        logger.info("Deleted temporary file: %s", file_path)
