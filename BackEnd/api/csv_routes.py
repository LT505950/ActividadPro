from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Any
import csv
import os
import json

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
    testMethodType: str
    respuestaGenerada: Optional[str] = ""
    chunks: Optional[List[Any]] = []  # ✅ PARA RAGAS

class SaveCSVRequest(BaseModel):
    ragActivo: str
    rows: List[CSVRow]

# ─────────────────────────────────────────────────────────
# SAVE CSV + JSON (MISMO ENDPOINT)
# ─────────────────────────────────────────────────────────

@router.post("/save")
def save_csv(payload: SaveCSVRequest):
    filename = CSV_MAP.get(payload.ragActivo)
    json_filename = JSON_MAP.get(payload.ragActivo)

    if not filename or not json_filename:
        raise HTTPException(status_code=400, detail="RAG inválido")

    os.makedirs(BASE_PATH, exist_ok=True)

    csv_path = os.path.join(BASE_PATH, filename)
    json_path = os.path.join(BASE_PATH, json_filename)

    # ─────────────────────────────
    # 1️⃣ GUARDAR CSV
    # ─────────────────────────────
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "question",
                "expectedResponse",
                "testMethodType",
                "respuestaGenerada",
            ])

            for row in payload.rows:
                writer.writerow([
                    row.question,
                    row.expectedResponse,
                    row.testMethodType,
                    row.respuestaGenerada or "",
                ])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando CSV: {str(e)}")

    # ─────────────────────────────
    # 2️⃣ GUARDAR JSON (INCREMENTAL)
    # ─────────────────────────────
    try:
        json_data = []

        # reconstruimos el estado ACTUAL (idempotente)
        for row in payload.rows:
            if not row.respuestaGenerada:
                continue  # ⛔ solo lo ya generado

            json_data.append({
                "question": row.question,
                "expectedResponse": row.expectedResponse,
                "testMethodType": row.testMethodType,
                "respuestaGenerada": row.respuestaGenerada,
                "chunks": row.chunks or [],
                "rag": payload.ragActivo,
            })

        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(json_data, jf, ensure_ascii=False, indent=2)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando JSON: {str(e)}")

    return {"ok": True}

# ─────────────────────────────────────────────────────────
# GET CSV
# ─────────────────────────────────────────────────────────

@router.get("/get/{ragActivo}")
def get_csv(ragActivo: str):
    filename = CSV_MAP.get(ragActivo)

    if not filename:
        raise HTTPException(status_code=400, detail="RAG inválido")

    file_path = os.path.join(BASE_PATH, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CSV no encontrado")

    return FileResponse(
        file_path,
        media_type="text/csv",
        filename=filename
    )