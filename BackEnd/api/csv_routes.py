from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
import csv
import os
import json
import shutil
import re

router = APIRouter(prefix="/csv", tags=["csv"])

# ─────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────

BASE_PATH = os.path.join(os.getcwd(), "data", "evaluacion")

CSV_MAP = {
    "actividadpro": "evaluar_helpdesk.csv",
    "carbot": "evaluar_carbot.csv",
}

JSON_MAP = {
    "actividadpro": "evaluar_helpdesk.json",
    "carbot": "evaluar_carbot.json",
}

# ─────────────────────────────────────────────────────────
# MODELOS
# ─────────────────────────────────────────────────────────

class CSVRow(BaseModel):
    question: str
    expectedResponse: str
    actualResponse: Optional[str] = ""
    chunks: Optional[List[Any]] = []

class SaveCSVRequest(BaseModel):
    ragActivo: str
    rows: List[CSVRow]

class GuardarVersionRequest(BaseModel):
    ragActivo: str

# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────

def get_next_version(folder: str, base_name: str) -> int:
    pattern = re.compile(rf"{base_name}_v(\d+)\.csv")
    versions = []

    for f in os.listdir(folder):
        m = pattern.fullmatch(f)
        if m:
            versions.append(int(m.group(1)))

    return max(versions, default=0) + 1

# ─────────────────────────────────────────────────────────
# GET CSV BASE
# ─────────────────────────────────────────────────────────

@router.get("/get/{ragActivo}")
def get_csv_base(ragActivo: str):
    csv_name = CSV_MAP.get(ragActivo)
    if not csv_name:
        raise HTTPException(400, "RAG inválido")

    rag_path = os.path.join(BASE_PATH, ragActivo)
    csv_path = os.path.join(rag_path, csv_name)

    if not os.path.exists(csv_path):
        raise HTTPException(404, "CSV base no encontrado")

    rows = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "question": r.get("question", ""),
                "expectedResponse": r.get("expectedResponse", ""),
                "actualResponse": r.get("actualResponse", ""),
            })

    return {"rows": rows}

# ─────────────────────────────────────────────────────────
# SAVE CSV + JSON (INCREMENTAL, COMO ANTES)
# ─────────────────────────────────────────────────────────

@router.post("/save")
def save_csv_base(payload: SaveCSVRequest):
    csv_name = CSV_MAP.get(payload.ragActivo)
    json_name = JSON_MAP.get(payload.ragActivo)

    if not csv_name or not json_name:
        raise HTTPException(400, "RAG inválido")

    rag_path = os.path.join(BASE_PATH, payload.ragActivo)
    os.makedirs(rag_path, exist_ok=True)

    csv_path = os.path.join(rag_path, csv_name)
    json_path = os.path.join(rag_path, json_name)

    # ─────────────────────────────
    # 1️⃣ GUARDAR CSV
    # ─────────────────────────────
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["question", "expectedResponse", "actualResponse"])
            for row in payload.rows:
                writer.writerow([
                    row.question,
                    row.expectedResponse,
                    row.actualResponse or "",
                ])
    except Exception as e:
        raise HTTPException(500, f"Error guardando CSV: {str(e)}")

    # ─────────────────────────────
    # 2️⃣ GUARDAR JSON (INCREMENTAL ✅)
    # ─────────────────────────────
    try:
        json_data = []

        for row in payload.rows:
            if not row.actualResponse:
                continue  # solo respuestas generadas

            json_data.append({
                "question": row.question,
                "expectedResponse": row.expectedResponse,
                "actualResponse": row.actualResponse,
                "chunks": row.chunks or [],
                "rag": payload.ragActivo,
            })

        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(json_data, jf, ensure_ascii=False, indent=2)

    except Exception as e:
        raise HTTPException(500, f"Error guardando JSON: {str(e)}")

    return {"ok": True}

# ─────────────────────────────────────────────────────────
# GUARDAR VERSIÓN + LIMPIAR BASE
# ─────────────────────────────────────────────────────────

@router.post("/guardar-version")
def guardar_version(payload: GuardarVersionRequest):
    rag = payload.ragActivo
    csv_base = CSV_MAP.get(rag)
    json_base = JSON_MAP.get(rag)

    if not csv_base or not json_base:
        raise HTTPException(400, "RAG inválido")

    rag_path = os.path.join(BASE_PATH, rag)
    csv_path = os.path.join(rag_path, csv_base)
    json_path = os.path.join(rag_path, json_base)

    if not os.path.exists(csv_path):
        raise HTTPException(404, "CSV base no encontrado")

    base_name = csv_base.replace(".csv", "")
    version = get_next_version(rag_path, base_name)

    # copiar CSV y JSON
    shutil.copyfile(csv_path, os.path.join(rag_path, f"{base_name}_v{version}.csv"))
    shutil.copyfile(json_path, os.path.join(rag_path, f"{base_name}_v{version}.json"))

    # limpiar CSV base
    cleaned = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            cleaned.append([r["question"], r["expectedResponse"], ""])

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["question", "expectedResponse", "actualResponse"])
        writer.writerows(cleaned)

    # limpiar JSON base
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump([], jf, ensure_ascii=False, indent=2)

    return {"ok": True, "version": f"v{version}"}