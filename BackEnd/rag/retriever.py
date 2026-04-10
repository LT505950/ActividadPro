from services.embedding_service import get_embedding
from services.qdrant_service import search_qdrant

# ✅ Mapeo central de RAG → colección Qdrant
RAG_COLLECTIONS = {
    "actividadpro": "soporte_actividadpro",
    "carbot": "soporte_carbot"
}

def search_chunks(request):
    # 1️⃣ Obtener embedding
    embedding_vector = get_embedding(request.query)

    # 2️⃣ Resolver RAG (default seguro)
    rag = getattr(request, "rag", "actividadpro")
    collection = RAG_COLLECTIONS.get(rag, "soporte_actividadpro")

    # 3️⃣ Buscar en Qdrant (colección dinámica)
    data = search_qdrant(
        vector=embedding_vector,
        top=request.top,
        collection=collection
    )
    # 4️⃣ Normalizar chunks
    chunks = [
        {
            "id": str(point.get("id")),
            "text": point.get("payload", {}).get("text", ""),
            "source": point.get("payload", {}).get("source", "desconocida")
        }
        for point in data.get("result", [])
    ]

    return {"chunks": chunks}
