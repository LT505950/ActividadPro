import os
import ollama
from dotenv import load_dotenv

load_dotenv()

def generate_answer_stream(prompt: str):
    """Generador que hace streaming token a token desde Ollama y al final emite info de tokens"""
    stream = ollama.chat(
        model=os.getenv("OLLAMA_CHAT_MODEL", "gemma4:e2b"),
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    prompt_tokens = 0
    completion_tokens = 0

    for chunk in stream:
        token = chunk["message"]["content"]
        if token:
            yield {"type": "token", "value": token}

        # Ollama incluye las estadísticas en el último chunk (done=True)
        if chunk.get("done"):
            prompt_tokens = chunk.get("prompt_eval_count", 0)
            completion_tokens = chunk.get("eval_count", 0)

    # Al terminar el stream, emitir la info de tokens como evento especial
    yield {
        "type": "tokens_info",
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens
    }
