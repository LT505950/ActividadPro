# ─────────────────────────────────────────────
# FIXES CRÍTICOS PARA WINDOWS + PYTHON 3.11
# ─────────────────────────────────────────────
import os
import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
os.environ["RAGAS_DISABLE_ASYNC"] = "true"

# ─────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────
import time
import json
from pathlib import Path
from typing import List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

from datasets import (
    Dataset,
    Features,
    Value,
    Sequence,
)

from ragas import evaluate, RunConfig
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    faithfulness,
)

from langchain.embeddings.base import Embeddings
from services.deepseek_ragas_llm import DeepSeekGatewayLLM


# ─────────────────────────────────────────────
# ENV
# ─────────────────────────────────────────────
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL")
DIMENSIONS = int(os.getenv("VECTOR_SIZE"))

HEADERS = {
    "X-Gateway-API-Key": API_KEY,
    "Content-Type": "application/json",
}


# ─────────────────────────────────────────────
# SESSION HTTP CON RETRY
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# EMBEDDINGS REALES + LOGS
# ─────────────────────────────────────────────
_embedding_counter = 0

def get_embedding(text: str) -> List[float]:
    global _embedding_counter
    _embedding_counter += 1

    preview = text.replace("\n", " ")[:80]
    print(f"🧠 [EMB] #{_embedding_counter} → {preview}...")

    start = time.time()

    body = {
        "model": EMBED_MODEL,
        "input": text,
        "dimensions": DIMENSIONS
    }

    resp = session.post(
        f"{BASE_URL}/v1/embeddings",
        headers=HEADERS,
        json=body,
        timeout=(10, 60),  # 🔑 MUY IMPORTANTE
    )

    resp.raise_for_status()

    elapsed = time.time() - start
    print(f"✅ [EMB] #{_embedding_counter} OK ({elapsed:.2f}s)")

    time.sleep(0.05)
    return resp.json()["data"][0]["embedding"]


# ─────────────────────────────────────────────
# ADAPTER LANGCHAIN → RAGAS
# ─────────────────────────────────────────────
class GatewayEmbeddings(Embeddings):
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [get_embedding(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return get_embedding(text)


# ─────────────────────────────────────────────
# DATASET (SCHEMA CORRECTO PARA RAGAS)
# ─────────────────────────────────────────────
#DATASET_PATH = Path("data/evaluacion/evaluar_carbot.json")
DATASET_PATH = Path("data/evaluacion/evaluar_helpdesk.json")

def load_ragas_dataset() -> Dataset:
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    rows = []

    # 🔎 IMPORTANTE: limita a pocos registros mientras depuras
    for item in raw_data:
        contexts = [
            c["text"]
            for c in item.get("chunks", [])
            if isinstance(c.get("text"), str) and c.get("text").strip()
        ]

        rows.append({
            "question": str(item.get("question", "")),
            "answer": str(item.get("respuestaGenerada", "")),
            "ground_truth": str(item.get("expectedResponse", "")),
            "contexts": contexts,
        })

    # ✅ SCHEMA EXPLÍCITO (OBLIGATORIO PARA RAGAS)
    features = Features({
        "question": Value("string"),
        "answer": Value("string"),
        "ground_truth": Value("string"),
        "contexts": Sequence(Value("string")),
    })

    return Dataset.from_list(rows, features=features)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 DEBUG RAGAS — INICIO\n")

    dataset = load_ragas_dataset()
    print(f"📦 Registros cargados: {len(dataset)}\n")

    llm = DeepSeekGatewayLLM()
    embeddings = GatewayEmbeddings()

    print("▶ Métricas:")
    print("  - answer_relevancy")
    print("  - context_precision\n")
    print("  - faithfulness\n")

    run_config = RunConfig(
        max_workers=1,   # 🔑 FORZAR SECUENCIAL
        timeout=300,
        max_wait=300,
    )

    start = time.time()

    result = evaluate(
        dataset=dataset,
        metrics=[
            answer_relevancy,
            context_precision,
            faithfulness,
        ],
        llm=llm,
        embeddings=embeddings,
        run_config=run_config,
        raise_exceptions=True,
    )

    elapsed = time.time() - start

    print("\n✅ EVALUACIÓN TERMINADA")
    print(f"⏱ Tiempo total: {elapsed:.2f}s\n")
    print(result)

    output_path = Path("data/evaluacion/resultados_ragas_helpdesk.csv")
    result.to_pandas().to_csv(output_path, index=False, encoding="utf-8")
    print(f"\n💾 Resultados guardados en: {output_path}")
