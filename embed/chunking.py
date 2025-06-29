def split_text_into_chunks(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """
    Splits text into overlapping chunks for vector embedding.

    :param text: Full document text
    :param chunk_size: Number of words per chunk
    :param overlap: Number of words to overlap between chunks
    :return: List of text chunks
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
    return chunks
