from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings

def get_character_text_splitter(
    chunk_size: int = settings.CHUNK_SIZE, 
    chunk_overlap: int = settings.CHUNK_OVERLAP
) -> RecursiveCharacterTextSplitter:
    """
    Initializes and returns a RecursiveCharacterTextSplitter instance.
    
    Note: BAAI/bge-small-en-v1.5 has a max token limit of 512. 
    A chunk_size of 800 characters keeps the text safely within token bounds.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False
    )
