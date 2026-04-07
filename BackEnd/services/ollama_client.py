import os
import ollama
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("OLLAMA_GENERATE_MODEL", "phi4-mini")

def generate_text(prompt: str) -> str:

    response = ollama.generate(
        model=MODEL,
        prompt=prompt
    )
    return response['response']