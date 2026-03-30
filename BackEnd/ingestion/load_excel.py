import pandas as pd
import os

def load_excel(file_path: str) -> list[dict]:
    """
    Carga datos de un archivo Excel y devuelve una lista de documentos para RAG.
    - Si tiene columnas 'Pregunta' / 'Respuesta' (case-insensitive), las usa directamente.
    - Si no, concatena todas las columnas disponibles como texto.
    Omite filas completamente vacías.
    """
    df = pd.read_excel(file_path)

    # Normalizar nombres de columnas a minúsculas para comparación segura
    df.columns = df.columns.str.strip().str.lower()

    docs = []
    source_name = os.path.basename(file_path)
    skipped = 0

    for _, row in df.iterrows():

        # Ignorar filas donde todo es NaN
        if row.isnull().all():
            skipped += 1
            continue

        # ── Caso pregunta-respuesta (tus Excel de soporte) ──────────────
        if 'pregunta' in df.columns and 'respuesta' in df.columns:
            pregunta  = str(row['pregunta']).strip()  if pd.notna(row['pregunta'])  else ""
            respuesta = str(row['respuesta']).strip() if pd.notna(row['respuesta']) else ""

            # Omitir fila si ambos campos están vacíos
            if not pregunta and not respuesta:
                skipped += 1
                continue

            text = f"Pregunta: {pregunta}\nRespuesta: {respuesta}"

        # ── Caso genérico: concatenar todas las columnas ─────────────────
        else:
            text_parts = []
            for col in df.columns:
                val = row[col]
                if pd.notna(val) and str(val).strip():
                    text_parts.append(f"{col}: {str(val).strip()}")

            if not text_parts:
                skipped += 1
                continue

            text = "\n".join(text_parts)  # separador legible entre columnas

        docs.append({
            "text": text,
            "source": source_name,
            "type": "excel"
        })

    print(f"📊 Excel '{source_name}': {len(docs)} filas cargadas, {skipped} omitidas")
    return docs