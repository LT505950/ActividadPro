def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Divide el texto en chunks de tamaño aproximado `chunk_size` caracteres,
    cortando siempre en el espacio más cercano para no partir palabras.
    Aplica overlap entre chunks para preservar contexto.
    """
    if not text or not text.strip():
        return []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size

        # Si no llegamos al final, busca el último espacio para no cortar palabras
        if end < text_len:
            cut = text.rfind(' ', start, end)
            if cut != -1:  # Si encontró un espacio, corta ahí
                end = cut

        chunk = text[start:end].strip()
        if chunk:  # Solo agrega si el chunk tiene contenido
            chunks.append(chunk)

        # Avanzar con overlap, también en un límite de palabra
        next_start = end - overlap
        # Buscar el siguiente espacio para que el overlap no parta palabras
        space = text.find(' ', next_start)
        start = space + 1 if space != -1 and space < end else end

    return chunks