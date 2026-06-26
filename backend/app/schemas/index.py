from pydantic import BaseModel

class IndexResult(BaseModel):
    chunks: int
    collection: str
    filename: str
    status: str
