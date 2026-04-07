import os
import ollama
from dotenv import load_dotenv

load_dotenv()

def get_embedding(text: str):
    response = ollama.embeddings(
        model=os.getenv("OLLAMA_EMBED_MODEL", "bge-m3"),
        prompt=text
    )
    return response["embedding"]