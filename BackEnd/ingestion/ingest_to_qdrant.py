import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from load_md import load_md
from load_excel import load_excel
from chunking import chunk_text
from embedding import get_embedding

# ── CONFIG ──────────────────────────────────────────────────
QDRANT_HOST      = "localhost"
QDRANT_PORT      = 6333
COLLECTION_NAME  = "soporte_actividadpro"

# Dimensiones del modelo nomic-embed-text (fijado por el modelo, NO cambiar
# a menos que cambies de modelo de embedding)
VECTOR_SIZE      = 1024

# Cuántos puntos subir a Qdrant por petición (evita timeouts y picos de RAM)
BATCH_SIZE       = 100

# ── INIT CLIENT ─────────────────────────────────────────────
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


# ── CREAR COLECCIÓN ─────────────────────────────────────────
def create_collection():
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
        print("✅ Colección creada")
    else:
        print("⚠️  La colección ya existe, se reutiliza")


# ── CARGAR DATOS ────────────────────────────────────────────
def load_all_data() -> list[dict]:
    docs = []

    BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    md_path    = os.path.join(BASE_DIR, "data", "md")
    excel_path = os.path.join(BASE_DIR, "data", "excel")

    if not os.path.exists(md_path):
        raise FileNotFoundError(f"❌ No existe la carpeta MD: {md_path}")
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"❌ No existe la carpeta Excel: {excel_path}")

    # Cargar archivos Markdown
    docs.extend(load_md(md_path))

    # Cargar archivos Excel
    for file in os.listdir(excel_path):
        if file.endswith(".xlsx"):
            docs.extend(load_excel(os.path.join(excel_path, file)))

    print(f"📄 Total documentos cargados: {len(docs)}")
    return docs


# ── SUBIDA EN BATCHES ───────────────────────────────────────
def upload_batch(points: list[PointStruct]):
    """Sube una lista de PointStruct a Qdrant en bloques de BATCH_SIZE."""
    total = len(points)
    for i in range(0, total, BATCH_SIZE):
        batch = points[i : i + BATCH_SIZE]
        client.upsert(collection_name=COLLECTION_NAME, points=batch)
        print(f"   ↑ Subidos {min(i + BATCH_SIZE, total)}/{total} puntos")


# ── INGESTA PRINCIPAL ────────────────────────────────────────
def ingest():
    docs   = load_all_data()
    points = []
    point_id = 1
    skipped  = 0

    for doc in docs:
        chunks = chunk_text(doc["text"])

        for chunk in chunks:
            try:
                vector = get_embedding(chunk)

                # Payload: omite campos vacíos para no ensuciar los filtros
                payload = {
                    k: v for k, v in {
                        "text":    chunk,
                        "source":  doc.get("source", ""),
                        "type":    doc.get("type", ""),
                        "modulo":  doc.get("modulo"),
                        "error":   doc.get("error"),
                        "version": doc.get("version"),
                    }.items() if v  # excluye None y ""
                }

                # ✅ Usar PointStruct en lugar de dicts crudos
                points.append(PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                ))
                point_id += 1

            except Exception as e:
                print(f"❌ Error en chunk (doc: {doc.get('source', '?')}): {e}")
                skipped += 1

    print(f"\n📦 Total puntos generados : {len(points)}")
    print(f"⚠️  Chunks omitidos por error: {skipped}")

    if points:
        upload_batch(points)
        print("✅ Ingesta completada")
    else:
        print("⚠️  No hay puntos para subir")


# ── ENTRY POINT ──────────────────────────────────────────────
if __name__ == "__main__":
    create_collection()
    ingest()