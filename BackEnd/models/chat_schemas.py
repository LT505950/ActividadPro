from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    query: str

class Source(BaseModel):
    text: str
    source: str

class ChatResponse(BaseModel):
    answer: str
    chunks: List[Source]