from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    query: str
    top: int = 3

class Chunk(BaseModel):
    id: str
    text: str
    source: str

class SearchResponse(BaseModel):
    chunks: List[Chunk]