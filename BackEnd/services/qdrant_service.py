import os
import requests
from dotenv import load_dotenv

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")

def search_qdrant(vector, top: int, collection: str):
    url = f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{collection}/points/search"

    payload = {
        "vector": vector,
        "top": top,
        "with_payload": True,
        #"score_threshold": 0.75
    }

    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()