import os
import ollama
from typing import List
from dotenv import load_dotenv

load_dotenv()

def get_embedding(text: str) -> List[float]:
    """
    Obtiene el embedding de un texto usando el modelo configurado en OLLAMA_EMBED_MODEL.
    """
    try:
        response = ollama.embeddings(
            model=os.getenv("OLLAMA_EMBED_MODEL", "bge-m3"),
            prompt=text
        )
        return response["embedding"]

    except KeyError:
        raise ValueError("La respuesta de Ollama no contiene 'embedding'.")
    except Exception as e:
        raise RuntimeError(f"Error al generar embedding: {str(e)}")