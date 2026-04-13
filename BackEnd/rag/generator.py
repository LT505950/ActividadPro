from services.ollama_client import generate_text


def generate_answer_stream(prompt: str):
    """
    Respuesta NO en streaming real.
    Compatible con el frontend SSE actual.
    """

    try:
        full_text = generate_text(prompt)

        # ✅ CLAVE CORRECTA: value
        yield {
            "type": "token",
            "value": full_text
        }

        prompt_tokens = len(prompt.split())
        completion_tokens = len(full_text.split())

        yield {
            "type": "tokens_info",
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens
        }

    except Exception:
        yield {
            "type": "token",
            "value": "Error al generar la respuesta."
        }