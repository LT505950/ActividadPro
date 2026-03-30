import os
import re

def load_md(folder_path: str) -> list[dict]:
    """
    Carga archivos .md desde una carpeta.
    Extrae el nombre del source del comentario <!-- Source: ... --> si existe.
    Omite archivos vacíos.
    """
    documents = []

    for filename in os.listdir(folder_path):
        if not filename.endswith(".md"):
            continue

        full_path = os.path.join(folder_path, filename)

        with open(full_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Ignorar archivos vacíos
        if not text.strip():
            print(f"⚠️  Archivo vacío ignorado: {filename}")
            continue

        # Extraer el nombre del source del comentario HTML si existe
        # Ejemplo: <!-- Source: Actividad PRO Manual 1_P31_consulta.md -->
        source_match = re.search(r'<!--\s*Source:\s*(.+?)\s*-->', text)
        source_name = source_match.group(1).strip() if source_match else filename

        documents.append({
            "text": text,
            "source": source_name,   # nombre real del documento original
            "type": "md"
        })

    print(f"📄 MD cargados: {len(documents)}")
    return documents