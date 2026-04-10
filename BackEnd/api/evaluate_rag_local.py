import json
import os
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

from langchain_ollama import OllamaLLM, OllamaEmbeddings

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

BASE_PATH = os.path.join(os.getcwd(), "data", "evaluacion")

RAG = "actividadpro"  # o "carbot"

JSON_FILE_MAP = {
    "actividadpro": "evaluar_helpdesk.json",
    "carbot": "evaluar_carbot.json",
}

JSON_PATH = os.path.join(BASE_PATH, JSON_FILE_MAP[RAG])

# MODELOS LOCALES
LLM_MODEL = "qwen3:0.6b"
EMBED_MODEL = "bge-m3"

# ─────────────────────────────────────────────
# LOAD JSON
# ─────────────────────────────────────────────

if not os.path.exists(JSON_PATH):
    raise FileNotFoundError(f"No existe el archivo: {JSON_PATH}")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

if not raw_data:
    raise ValueError("El JSON está vacío")

print(f"📄 Filas totales en JSON: {len(raw_data)}")

# ─────────────────────────────────────────────
# TRANSFORM DATA FOR RAGAS
# ─────────────────────────────────────────────

ragas_rows = []

for idx, row in enumerate(raw_data):
    contexts = []

    for c in row.get("chunks", []):
        if not isinstance(c, dict):
            continue

        content = (
            c.get("content")
            or c.get("text")
            or c.get("page_content")
        )

        if content:
            contexts.append(content)

    if not contexts:
        print(f"⚠️ Fila {idx} descartada: sin chunks")
        continue

    if not row.get("respuestaGenerada"):
        print(f"⚠️ Fila {idx} descartada: sin respuestaGenerada")
        continue

    ragas_rows.append({
        "question": row["question"],
        "answer": row["respuestaGenerada"],
        "contexts": contexts,
        "ground_truth": row["expectedResponse"],
    })

print(f"✅ Filas válidas para RAGAS: {len(ragas_rows)}")

if not ragas_rows:
    raise ValueError("No hay filas válidas para RAGAS")

dataset = Dataset.from_list(ragas_rows)

# ─────────────────────────────────────────────
# INIT MODELOS LOCALES
# ─────────────────────────────────────────────

llm = OllamaLLM(
    model=LLM_MODEL,
    temperature=0,
)

embeddings = OllamaEmbeddings(
    model=EMBED_MODEL,
)

# ─────────────────────────────────────────────
# RUN RAGAS (VERSIÓN COMPATIBLE)
# ─────────────────────────────────────────────

results = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ],
    llm=llm,
    embeddings=embeddings,
)

# ─────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────

print("\n✅ RESULTADOS RAGAS (100% LOCAL)\n")
for metric, score in results.items():
    print(f"{metric}: {round(score, 4)}")

# ─────────────────────────────────────────────
# SAVE RESULTS
# ─────────────────────────────────────────────

output_path = os.path.join(
    BASE_PATH,
    f"ragas_results_{RAG}_local.json"
)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n📄 Resultados guardados en: {output_path}")