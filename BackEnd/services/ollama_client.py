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

session = requests.Session()

retries = Retry(
    total=3,
    backoff_factor=1.0,
    status_forcelist=[429, 502, 503, 504],
    allowed_methods=["POST"],
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)


def generate_text(prompt: str) -> str:
    body = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
    }

    try:
        resp = session.post(
            f"{BASE_URL}/v1/chat/completions",
            headers=HEADERS,
            json=body,
            timeout=(10, 60),
        )

        if resp.status_code != 200:
            raise RuntimeError(
                f"Error generación {resp.status_code}: {resp.text}"
            )

        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error de red generación: {e}")

    finally:
        time.sleep(0.05)