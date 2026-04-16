from rag.retriever import search_chunks
from rag.prompt_builder import build_prompt
from rag.generator import generate_answer_stream
import os
import dotenv
dotenv.load_dotenv()
TOP_K = int(os.getenv("TOP_K"))

def run_rag_stream(query: str, rag: str):
    """Retorna los chunks y un generador de eventos (tokens + tokens_info) para streaming"""
    result = search_chunks(type("obj", (object,), {"query": query, "top": TOP_K, "rag": rag}))
    chunks = result["chunks"]
    prompt = build_prompt(query, chunks, rag)
    token_generator = generate_answer_stream(prompt)
    return chunks, token_generator
