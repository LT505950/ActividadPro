import ollama

def generate_answer_stream(prompt: str):
    """Generador que hace streaming token a token desde Ollama"""
    stream = ollama.chat(
        model="gemma4:e2b",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    for chunk in stream:
        token = chunk["message"]["content"]
        if token:
            yield token