from langchain_community.document_loaders import PyMuPDFLoader
from pathlib import Path

def get_document_loader(file_path: str) -> PyMuPDFLoader:
    """
    Initializes and returns a PyMuPDFLoader instance for the given PDF file path.
    PyMuPDF is one of the fastest and most accurate parsing options available.
    """
    Path(file_path).suffix.lower()
    
    return PyMuPDFLoader(file_path=file_path)
