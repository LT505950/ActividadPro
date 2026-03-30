import ollama
from typing import List

def get_embedding(text: str) -> List[float]:
    """
    Obtiene el embedding de un texto usando el modelo 'nomic-embed-text:latest'.
    """
    try:
        response = ollama.embeddings(
            model="bge-m3",
            prompt=text
        )
        return response["embedding"]

    except KeyError:
        raise ValueError("La respuesta de Ollama no contiene 'embedding'.")
    except Exception as e:
        raise RuntimeError(f"Error al generar embedding: {str(e)}")