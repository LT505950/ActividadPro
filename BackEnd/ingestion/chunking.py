def chunk_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 70
) -> list[str]:

    if not text or not text.strip():
        return []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)

        # cortar por palabra si no está al final
        if end < text_len:
            cut = text.rfind(" ", start, end)
            if cut > start:
                end = cut

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # 🚨 CLAVE: forzar avance real
        new_start = end - overlap
        if new_start <= start:
            new_start = end  # fuerza avance

        start = new_start

    return chunks