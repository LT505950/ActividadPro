from services.embedding_service import get_embedding
from services.qdrant_service import search_qdrant

def search_chunks(request):
    embedding_vector = get_embedding(request.query)

    data = search_qdrant(embedding_vector, request.top)

    chunks = [
        {
            "id": str(point.get("id")),
            "text": point.get("payload", {}).get("text", ""),
            "source": point.get("payload", {}).get("source", "desconocida")
        }
        for point in data.get("result", [])
    ]

    return {"chunks": chunks}