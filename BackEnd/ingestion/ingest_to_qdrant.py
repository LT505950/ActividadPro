import os
import time
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from load_md import load_md
from load_excel import load_excel
from chunking import chunk_text
from embedding import get_embedding

load_dotenv()

# ── CONFIG ──────────────────────────────────────────────────
QDRANT_HOST     = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT     = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "soporte_actividadpro"

# ✅ dimensión real comprobada en tu gateway
VECTOR_SIZE = 1024

BATCH_SIZE = 100

# ── INIT CLIENT ─────────────────────────────────────────────
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


# ── RECREAR COLECCIÓN ──────────────────────────────────────
def recreate_collection():
    collections = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME in collections:
        print("🗑️  Eliminando colección existente...", flush=True)
        client.delete_collection(collection_name=COLLECTION_NAME)

    print("🆕 Creando colección nueva...", flush=True)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )
    print("✅ Colección recreada correctamente", flush=True)


# ── CARGAR DATOS ────────────────────────────────────────────
def load_all_data() -> list[dict]:
    docs = []

    BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    md_path    = os.path.join(BASE_DIR, "data", "md")
    excel_path = os.path.join(BASE_DIR, "data", "excel")

    docs.extend(load_md(md_path))

    for file in os.listdir(excel_path):
        if file.endswith(".xlsx"):
            docs.extend(load_excel(os.path.join(excel_path, file)))

    print(f"📄 Total documentos cargados: {len(docs)}", flush=True)
    return docs


# ── SUBIDA EN BATCHES ───────────────────────────────────────
def upload_batch(points: list[PointStruct]):
    total = len(points)
    for i in range(0, total, BATCH_SIZE):
        batch = points[i:i + BATCH_SIZE]
        print(f"🚀 Subiendo batch {i//BATCH_SIZE + 1} ({len(batch)} puntos)", flush=True)
        client.upsert(collection_name=COLLECTION_NAME, points=batch)


# ── RETRY SOLO DE FALLIDOS ──────────────────────────────────
def retry_failed_chunks(failed_chunks, start_point_id):
    print(f"\n🔁 Reintentando {len(failed_chunks)} chunks fallidos...\n", flush=True)

    retry_points = []
    point_id = start_point_id

    for idx, item in enumerate(failed_chunks, start=1):
        doc = item["doc"]
        chunk = item["chunk"]

        print(f"   🔄 Retry {idx}/{len(failed_chunks)}", flush=True)

        try:
            vector = get_embedding(chunk)

            payload = {
                k: v for k, v in {
                    "text": chunk,
                    "source": doc.get("source"),
                    "type": doc.get("type"),
                    "modulo": doc.get("modulo"),
                    "error": doc.get("error"),
                    "version": doc.get("version"),
                }.items() if v
            }

            retry_points.append(PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            ))
            point_id += 1

            # más suave en retries
            time.sleep(0.2)

        except Exception as e:
            print(f"      ❌ Retry fallido definitivo: {e}", flush=True)

    return retry_points


# ── INGESTA PRINCIPAL CON DEBUG ─────────────────────────────
def ingest():
    docs = load_all_data()

    points = []
    failed_chunks = []

    point_id = 1
    skipped = 0
    embedding_count = 0

    for doc_idx, doc in enumerate(docs, start=1):
        print(f"\n📘 Documento {doc_idx}/{len(docs)}: {doc.get('source')}", flush=True)

        chunks = chunk_text(doc["text"])
        print(f"   🔹 Chunks generados: {len(chunks)}", flush=True)

        for chunk_idx, chunk in enumerate(chunks, start=1):
            embedding_count += 1

            print(
                f"      ▶ Embedding #{embedding_count} "
                f"(doc {doc_idx}, chunk {chunk_idx}/{len(chunks)})",
                flush=True
            )

            start = time.time()

            try:
                print("         ⏳ Llamando a get_embedding...", flush=True)
                vector = get_embedding(chunk)
                elapsed = time.time() - start

                print(f"         ✅ Embedding OK ({elapsed:.2f}s)", flush=True)

                payload = {
                    k: v for k, v in {
                        "text": chunk,
                        "source": doc.get("source"),
                        "type": doc.get("type"),
                        "modulo": doc.get("modulo"),
                        "error": doc.get("error"),
                        "version": doc.get("version"),
                    }.items() if v
                }

                points.append(PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                ))
                point_id += 1

            except Exception as e:
                elapsed = time.time() - start
                print(
                    f"         ❌ ERROR embedding "
                    f"(tardó {elapsed:.2f}s): {e}",
                    flush=True
                )

                failed_chunks.append({
                    "doc": doc,
                    "chunk": chunk
                })
                skipped += 1

    print(f"\n📦 Total puntos iniciales : {len(points)}", flush=True)
    print(f"⚠️  Chunks fallidos       : {skipped}", flush=True)

    # ── SUBIDA PRINCIPAL ─────────────────────────────────────
    if points:
        upload_batch(points)

    # ── RETRY FINAL ──────────────────────────────────────────
    if failed_chunks:
        retry_points = retry_failed_chunks(failed_chunks, point_id)
        if retry_points:
            upload_batch(retry_points)
            print(f"✅ Retry completado ({len(retry_points)} recuperados)", flush=True)
        else:
            print("⚠️  Ningún chunk fallido pudo recuperarse", flush=True)

    print("✅ Ingesta finalizada", flush=True)


# ── ENTRY POINT ─────────────────────────────────────────────
if __name__ == "__main__":
    recreate_collection()
    ingest()