from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import StreamingResponse
from typing import Optional
import os
import uuid
import json
import easyocr

from models.schema import SearchRequest, SearchResponse
from rag.retriever import search_chunks
from rag.pipeline import run_rag_stream

router = APIRouter()
reader = easyocr.Reader(['es'])

# ─────────────────────────────────────────────────────────
# SEARCH (sin cambios)
# ─────────────────────────────────────────────────────────
@router.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    return search_chunks(req)

# ─────────────────────────────────────────────────────────
# CHAT CON STREAMING + RAG
# ─────────────────────────────────────────────────────────
@router.post("/chat")
async def chat(
    request: Request,
    query: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    # ── 1. Detectar JSON o FormData ──
    if query is None:
        try:
            body = await request.json()
            query = body.get("query", "")
        except Exception:
            query = ""

    query = query or ""

    # ── 2. OCR si viene imagen ──
    if file:
        temp_path = f"temp_{uuid.uuid4()}.png"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        try:
            result = reader.readtext(temp_path)
            texto_ocr = " ".join([r[1] for r in result])
            texto_ocr = texto_ocr.replace("\n", " ").strip()

            if not texto_ocr:
                texto_ocr = "No se detectó texto en la imagen"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        final_query = f'Pregunta: "{query}"\nTexto detectado en imagen: "{texto_ocr}"'
    else:
        final_query = query

    # ── 3. Ejecutar RAG con streaming ──
    chunks, token_generator = run_rag_stream(final_query)

    def event_stream():
        # 🔹 Mandamos primero los chunks (metadata RAG)
        yield (
            "data: "
            + json.dumps(
                {"type": "chunks", "chunks": chunks},
                ensure_ascii=False
            )
            + "\n\n"
        )

        # 🔹 Iteramos el generador: puede emitir tokens o tokens_info
        for event in token_generator:
            if event["type"] == "token":
                # Token de texto normal
                yield (
                    "data: "
                    + json.dumps(
                        {"type": "token", "token": event["value"]},
                        ensure_ascii=False
                    )
                    + "\n\n"
                )
            elif event["type"] == "tokens_info":
                # Estadísticas de tokens al final
                yield (
                    "data: "
                    + json.dumps(
                        {
                            "type": "tokens_info",
                            "prompt_tokens": event["prompt_tokens"],
                            "completion_tokens": event["completion_tokens"],
                            "total_tokens": event["total_tokens"]
                        },
                        ensure_ascii=False
                    )
                    + "\n\n"
                )

        # 🔹 Evento de fin
        yield (
            "data: "
            + json.dumps({"type": "end"})
            + "\n\n"
        )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 🔥 CRÍTICO para streaming
        }
    )
