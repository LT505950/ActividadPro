from fastapi import APIRouter, HTTPException
from pathlib import Path
import pandas as pd

router = APIRouter(prefix="/ragas", tags=["RAGAS Dashboard"])

BASE_PATH = Path("data/evaluacion")

RAG_FILES = {
    "actividadpro": BASE_PATH / "resultados_ragas_actividadpro.csv",
    "carbot": BASE_PATH / "resultados_ragas_carbot.csv",
}

@router.get("/dashboard/{rag}")
def get_ragas_dashboard(rag: str):
    if rag not in RAG_FILES:
        raise HTTPException(status_code=400, detail="RAG inválido")

    csv_path = RAG_FILES[rag]

    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Resultados RAGAS no disponibles")

    df = pd.read_csv(csv_path)

    # Métricas agregadas
    summary = {
        "answer_relevancy": round(df["answer_relevancy"].mean(), 4) if "answer_relevancy" in df else None,
        "context_precision": round(df["context_precision"].mean(), 4) if "context_precision" in df else None,
        "faithfulness": round(df["faithfulness"].mean(), 4) if "faithfulness" in df else None,
        "answer_correctness": round(df["answer_correctness"].mean(), 4) if "answer_correctness" in df else None,
    }

    # Tabla completa
    records = df.fillna("").to_dict(orient="records")

    return {
        "summary": summary,
        "rows": records,
    }
