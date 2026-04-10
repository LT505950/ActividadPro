import os
import time
from typing import List
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL")

HEADERS = {
    "X-Gateway-API-Key": API_KEY,
    "Content-Type": "application/json",
}

# ── SESSION CON REINTENTOS ─────────────────────────────────
session = requests.Session()

retries = Retry(
    total=5,
    backoff_factor=0.5,      # espera: 0.5s, 1s, 2s, 4s...
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["POST"]
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

# ── EMBEDDING ──────────────────────────────────────────────
def get_embedding(text: str) -> List[float]:
    """
    Obtiene embeddings usando POST directo al gateway,
    con retry, reuse de conexión y protección anti-reset.
    """
    body = {
        "model": EMBED_MODEL,
        "input": text,
        "dimensions": 1024  # ✅ según lo que YA comprobaste que funciona
    }

    try:
        resp = session.post(
            f"{BASE_URL}/v1/embeddings",
            headers=HEADERS,
            json=body,
            timeout=(10, 60)  # (connect, read)
        )

        if resp.status_code != 200:
            raise RuntimeError(
                f"Error embeddings {resp.status_code}: {resp.text}"
            )

        # ✅ micro-pausa para no tumbar al gateway
        time.sleep(0.05)

        return resp.json()["data"][0]["embedding"]

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error de red embeddings: {e}")
