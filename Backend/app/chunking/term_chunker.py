from .chunk_metadata import create_chunk_metadata


def create_term_chunks(terms: list[dict]) -> list[dict]:
    """
    Convert terminology records into term-level chunks.
    """

    chunks = []

    for index, term in enumerate(terms, start=1):
        chunk_id = f"term_{index:06d}"

        chunk = create_chunk_metadata(
            chunk_id=chunk_id,
            text=term["term"],
            language=term["language"],
            domain=term["domain"],
            chunk_type="term",
            source_type=term.get("source_type", "terminology"),
            authority=term.get("authority", "unknown"),
            document_id=term.get("document_id"),
        )

        chunk["translation"] = term.get("translation")
        chunk["term_type"] = term.get("term_type")

        chunks.append(chunk)

    return chunks