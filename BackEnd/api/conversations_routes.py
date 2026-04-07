from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import StreamingResponse
from typing import Optional
import os
import uuid
import json
import easyocr
from time import perf_counter

from opentelemetry import trace
from conversations.conversation import Conversation
from conversations.storage import save_conversation
from rag.pipeline import run_rag_stream

router = APIRouter()
reader = easyocr.Reader(["es"])
tracer = trace.get_tracer(__name__)

# ─────────────────────────────────────────────────────────
# Estado en memoria (simple pero correcto)
# ─────────────────────────────────────────────────────────

active_conversations: dict[str, Conversation] = {}

# ─────────────────────────────────────────────────────────
# CHAT MULTI‑TURN + STREAMING + OPEN TELEMETRY
# ─────────────────────────────────────────────────────────

@router.post("/chat2/{session_id}")
async def chat_multiturn(
    session_id: str,
    request: Request,
    query: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    # ── 1. Resolver query (JSON o FormData)
    if query is None:
        try:
            body = await request.json()
            query = body.get("query", "")
        except Exception:
            query = ""

    query = query or ""

    # ── 2. OCR (sin cambios)
    if file:
        temp_path = f"temp_{uuid.uuid4()}.png"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        try:
            result = reader.readtext(temp_path)
            texto_ocr = " ".join([r[1] for r in result]).replace("\n", " ").strip()
            texto_ocr = texto_ocr or "No se detectó texto en la imagen"
        finally:
            os.remove(temp_path)

        final_query = f'Pregunta: "{query}"\nTexto detectado en imagen: "{texto_ocr}"'
    else:
        final_query = query

    # ── 3. Obtener / crear conversación
    conversation = active_conversations.get(session_id)
    if not conversation:
        conversation = Conversation(agent="actividad-pro-rag-v1")
        active_conversations[session_id] = conversation

    # ── 4. Trace de conversación
    with tracer.start_as_current_span(
        "conversation",
        attributes={
            "conversation.id": conversation.test_id,
        }
    ):
        # ── 5. Registrar turno usuario
        conversation.add_user_turn(final_query)
        turn_id = conversation.user_turns

        with tracer.start_as_current_span(
            "conversation.turn",
            attributes={
                "conversation.turn_id": turn_id,
            }
        ):
            # ── 6. RETRIEVAL
            retrieval_start = perf_counter()
            chunks, token_generator = run_rag_stream(final_query)
            retrieval_latency_ms = (perf_counter() - retrieval_start) * 1000

            retrieval_scores = [c.get("score", 0) for c in chunks]

            with tracer.start_as_current_span(
                "rag.retrieval",
                attributes={
                    "rag.chunking.strategy": "markdown",
                    "rag.chunking.chunk_size": 500,
                    "rag.chunking.overlap": 50,
                    "rag.vectordb.engine": "qdrant",
                    "rag.search.type": "semantic",
                    "rag.retrieval.top_k": len(chunks),
                    "rag.retrieval.max_score": max(retrieval_scores) if retrieval_scores else 0,
                    "rag.retrieval.latency_ms": retrieval_latency_ms,
                }
            ):
                pass

            # ── 7. STREAMING LLM (NO SE ROMPE)
            def event_stream():
                answer = ""
                tokens_info = {}

                llm_start = perf_counter()

                # ── metadata chunks
                yield "data: " + json.dumps(
                    {"type": "chunks", "chunks": chunks},
                    ensure_ascii=False
                ) + "\n\n"

                for event in token_generator:
                    if event["type"] == "token":
                        answer += event["value"]
                        yield "data: " + json.dumps(
                            {"type": "token", "token": event["value"]},
                            ensure_ascii=False
                        ) + "\n\n"

                    elif event["type"] == "tokens_info":
                        tokens_info = event
                        llm_latency_ms = (perf_counter() - llm_start) * 1000

                        with tracer.start_as_current_span(
                            "llm.generate",
                            attributes={
                                "llm.model": "gemma4:e2b",
                                "llm.provider": "ollama",
                                "llm.token_count.input": event.get("prompt_tokens", 0),
                                "llm.token_count.output": event.get("completion_tokens", 0),
                                "llm.token_count.total": event.get("total_tokens", 0),
                                "llm.latency_ms": llm_latency_ms,
                            }
                        ):
                            pass

                        yield "data: " + json.dumps(
                            {"type": "tokens_info", **event},
                            ensure_ascii=False
                        ) + "\n\n"

                # ── 8. Registrar respuesta final
                conversation.add_turn(
                    role="assistant",
                    content=answer,
                    metadata={
                        "llm_model": "gemma4:e2b",
                        "tokens_in": tokens_info.get("prompt_tokens", 0),
                        "tokens_out": tokens_info.get("completion_tokens", 0),
                        "total_tokens": tokens_info.get("total_tokens", 0),
                        "chunks_used": len(chunks),
                        "retrieval_scores": retrieval_scores,
                    }
                )

                # ── 9. Cierre conversación
                if conversation.reached_max_turns():
                    conversation.conversation_complete = True
                    conversation.completion_reason = "max_turns"

                    with tracer.start_as_current_span(
                        "conversation.persist",
                        attributes={
                            "conversation.id": conversation.test_id
                        }
                    ):
                        save_conversation(conversation)

                    active_conversations.pop(session_id, None)

                yield "data: " + json.dumps({"type": "end"}) + "\n\n"

            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                },
            )
