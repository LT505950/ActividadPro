import os
import requests
from dotenv import load_dotenv

load_dotenv()

QDRANT_HOST = os.getenv('QDRANT_HOST', 'localhost')
QDRANT_PORT = os.getenv('QDRANT_PORT', '6333')
QDRANT_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/soporte_actividadpro/points/search"

def search_qdrant(vector, top: int):
    payload = {
        "vector": vector,
        "top": top,
        "with_payload": True,
        "score_treshold": 0.75
    }

    resp = requests.post(QDRANT_URL, json=payload)
    resp.raise_for_status()

    return resp.json()