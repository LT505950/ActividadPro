import os

from pydantic import BaseModel
from typing import List
import dotenv
dotenv.load_dotenv()
TOP_K = int(os.getenv("TOP_K"))
class SearchRequest(BaseModel):
    query: str
    top: int = TOP_K

class Chunk(BaseModel):
    id: str
    text: str
    source: str

class SearchResponse(BaseModel):
    chunks: List[Chunk]