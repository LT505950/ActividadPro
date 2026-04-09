import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from load_txt import load_txt
from chunking import chunk_text
from embedding import get_embedding

load_dotenv()

# ───────────────── CONFIG ─────────────────
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLLECTION_NAME = "soporte_carbot"

VECTOR_SIZE = 1024   # bge-m3
BATCH_SIZE = 100
TXT_FOLDER = os.path.join(BASE_DIR, "data", "txt")

# ───────────────── CLIENT ─────────────────
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)   

# ───────────────── COLLECTION ────────────
def recreate_collection():
    collections = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME in collections:
        print(f"🗑️ Eliminando colección existente: {COLLECTION_NAME}")
        client.delete_collection(collection_name=COLLECTION_NAME)

    print(f"🆕 Creando colección: {COLLECTION_NAME}")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

# ───────────────── DATA LOAD ──────────────
def load_all_data() -> list[dict]:
    docs = load_txt(TXT_FOLDER)
    print(f"📚 Total de archivos TXT cargados: {len(docs)}")
    return docs

# ───────────────── UPLOAD ─────────────────
def upload_batch(points: list[PointStruct]):
    total = len(points)
    print(f"🚀 Subiendo {total} embeddings a Qdrant...")

    for i in range(0, total, BATCH_SIZE):
        batch = points[i:i + BATCH_SIZE]
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch
        )
        print(f"   ↑ Subidos {min(i + BATCH_SIZE, total)} / {total}")

# ───────────────── INGEST ──────────────────
def ingest():
    docs = load_all_data()

    points = []
    point_id = 1
    skipped = 0
    total_chunks = 0

    print("⚙️ Procesando documentos y generando embeddings...")

    for doc_index, doc in enumerate(docs, start=1):
        chunks = chunk_text(doc["text"])
        total_chunks += len(chunks)

        print(f"📄 Documento {doc_index}/{len(docs)} → {len(chunks)} chunks")

        for i, chunk in enumerate(chunks, start=1):
            try:
                vector = get_embedding(chunk)

                payload = {
                    "text": chunk,
                    "source": doc["source"],
                    "path": doc["path"],
                    "chunk_index": i
                }

                points.append(
                    PointStruct(
                        id=point_id,
                        vector=vector,
                        payload=payload
                    )
                )

                if point_id % 50 == 0:
                    print(f"   ✅ Embeddings generados: {point_id}")

                point_id += 1

            except Exception as e:
                skipped += 1
                print(f"⚠️ Chunk omitido: {e}")

    print(f"📊 Total chunks generados: {total_chunks}")
    print(f"⏭️ Chunks omitidos: {skipped}")

    upload_batch(points)

    print(f"✅ Ingesta finalizada correctamente")
    print(f"   🔢 Total embeddings: {len(points)}")

# ───────────────── MAIN ───────────────────
if __name__ == "__main__":
    recreate_collection()
    ingest()