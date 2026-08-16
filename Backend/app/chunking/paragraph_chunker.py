def create_paragraph_chunks(records: list[dict]) -> list[dict]:
    """
    Convert document paragraphs into paragraph-level chunks.
    """

    chunks = []

    for index, record in enumerate(records, start=1):

        chunk = {
            "chunk_id": f"paragraph_{index:06d}",
            "text": record["text"],
            "language": record["language"],
            "domain": record["domain"],
            "chunk_type": "paragraph",
            "source_type": record.get(
                "source_type",
                "domain_document"
            ),
            "authority": record.get(
                "authority",
                "unknown"
            ),
            "document_id": record.get("document_id"),
            "paragraph_id": record.get("paragraph_id", index)
        }

        chunks.append(chunk)

    return chunks