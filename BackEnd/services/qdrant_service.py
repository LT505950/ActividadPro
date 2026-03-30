import requests

QDRANT_URL = "http://localhost:6333/collections/soporte_actividadpro/points/search"

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