import ollama

def get_embedding(text: str):
    response = ollama.embeddings(
        model="bge-m3",
        prompt=text
    )
    return response["embedding"]