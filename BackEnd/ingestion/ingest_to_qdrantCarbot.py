import os
import time
import subprocess
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from load_txt import load_txt
from chunking import chunk_text
from embedding import get_embedding

# ───────────────── CARGA ENV ─────────────────
load_dotenv()

# ───────────────── CONFIG ────────────────────
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_CARBOT")
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE"))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXT_FOLDER = os.path.join(BASE_DIR, "data", "txt")

# ───────────────── CLIENT ────────────────────
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, timeout=60)

# ───────────────── CHECKS ────────────────────
def check_ollama():
    result = subprocess.run(
        ["ollama", "ps"],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        raise RuntimeError("❌ Ollama no tiene modelos activos. Ejecuta: ollama run bge-m3")

    print("✅ Ollama activo", flush=True)

# ───────────────── COLLECTION ────────────────
def recreate_collection():
    collections = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME in collections:
        print(f"🗑️ Eliminando colección existente: {COLLECTION_NAME}", flush=True)
        client.delete_collection(collection_name=COLLECTION_NAME)

    print(f"🆕 Creando colección: {COLLECTION_NAME}", flush=True)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

# ───────────────── DATA LOAD ─────────────────
def load_all_data() -> list[dict]:
    docs = load_txt(TXT_FOLDER)
    print(f"📚 Total de archivos TXT cargados: {len(docs)}", flush=True)
    return docs

# ───────────────── SAFE EMBEDDING ────────────
def get_embedding_safe(text: str, timeout_seconds: int = 40):
    start = time.time()

    if not text or not text.strip():
        raise ValueError("Texto vacío")

    while True:
        try:
            embedding = get_embedding(text)

            if not embedding or len(embedding) != VECTOR_SIZE:
                raise ValueError(f"Embedding inválido (size={len(embedding) if embedding else 0})")

            return embedding

        except Exception as e:
            if time.time() - start > timeout_seconds:
                raise TimeoutError(f"Timeout generando embedding: {e}")
            time.sleep(1)

# ───────────────── INGEST ────────────────────
def ingest():
    docs = load_all_data()
    point_id = 1
    skipped = 0

    print("\n⚙️ Ingesta documento por documento\n", flush=True)

    for doc_index, doc in enumerate(docs, start=1):
        print(f"📄 Documento {doc_index}/{len(docs)}", flush=True)

        text = doc.get("text", "")
        print(f"   📏 Longitud texto: {len(text)}", flush=True)

        if not text.strip():
            print("⚠️ Documento vacío, se omite\n", flush=True)
            skipped += 1
            continue

        chunks = chunk_text(text)
        print(f"   → {len(chunks)} chunks", flush=True)

        for chunk_index, chunk in enumerate(chunks, start=1):
            try:
                print(f"🧠 Doc {doc_index} | Chunk {chunk_index}/{len(chunks)}", flush=True)

                vector = get_embedding_safe(chunk)

                payload = {
                    "text": chunk,
                    "source": doc.get("source"),
                    "path": doc.get("path"),
                    "doc_index": doc_index,
                    "chunk_index": chunk_index
                }

                client.upsert(
                    collection_name=COLLECTION_NAME,
                    wait=True,
                    points=[
                        PointStruct(
                            id=point_id,
                            vector=vector,
                            payload=payload
                        )
                    ]
                )

                point_id += 1

            except Exception as e:
                skipped += 1
                print(f"⚠️ Chunk omitido (doc {doc_index}, chunk {chunk_index}): {e}", flush=True)
                continue

        print(f"✅ Documento {doc_index} terminado\n", flush=True)

    print("🎉 Ingesta finalizada correctamente", flush=True)
    print(f"🔢 Total embeddings: {point_id - 1}", flush=True)
    print(f"⏭️ Chunks omitidos: {skipped}", flush=True)

# ───────────────── MAIN ──────────────────────
if __name__ == "__main__":
    check_ollama()
    recreate_collection()
    ingest()
