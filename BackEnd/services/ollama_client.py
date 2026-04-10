import os
import time
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("GENERATE_MODEL")

if not BASE_URL or not API_KEY:
    raise ValueError("BASE_URL o API_KEY no están configurados")

HEADERS = {
    "X-Gateway-API-Key": API_KEY,
    "Content-Type": "application/json",
}

# ── SESSION CON REINTENTOS ─────────────────────────────────
session = requests.Session()

retries = Retry(
    total=5,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["POST"],
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

# ── GENERACIÓN DE TEXTO ────────────────────────────────────
def generate_text(prompt: str) -> str:
    """
    Genera texto usando POST directo al gateway (/v1/responses),
    con retry, reuse de conexión y sin SDKs.
    """

    body = {
        "model": MODEL,
        "input": prompt,
        "temperature": 0.2,
    }

    try:
        resp = session.post(
            f"{BASE_URL}/v1/responses",
            headers=HEADERS,
            json=body,
            timeout=(10, 120),
        )

        if resp.status_code != 200:
            raise RuntimeError(
                f"Error generación {resp.status_code}: {resp.text}"
            )

        data = resp.json()

        # ✅ extracción robusta del texto
        if "output_text" in data:
            return data["output_text"].strip()

        for block in data.get("output", []):
            for content in block.get("content", []):
                if content.get("type") == "output_text":
                    return content.get("text", "").strip()

        raise RuntimeError("No se pudo extraer texto de la respuesta")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error de red generación: {e}")
    finally:
        # micro pausa para no saturar gateway
        time.sleep(0.05)