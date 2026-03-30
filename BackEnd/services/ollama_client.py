import ollama

MODEL = "phi4-mini"

def generate_text(prompt: str) -> str:

    response = ollama.generate(
        model=MODEL,
        prompt=prompt
    )
    return response['response']