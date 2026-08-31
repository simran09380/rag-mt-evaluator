def create_sentence_chunks(records: list[dict]) -> list[dict]:
    """
    Convert translation records into sentence-level chunks.
    """

    chunks = []

    for record in records:

        sentence_id = str(record["id"])

        source_chunk = {
            "chunk_id": f"src_{sentence_id}",
            "text": record["source"],
            "language": record["source_lang"],
            "domain": record["domain"],
            "chunk_type": "sentence",
            "source_type": "translation_memory",
            "authority": "unknown",
            "sentence_id": sentence_id,
            "document_id": record.get("document_id"),
        }

        target_chunk = {
            "chunk_id": f"tgt_{sentence_id}",
            "text": record["reference"],
            "language": record["target_lang"],
            "domain": record["domain"],
            "chunk_type": "sentence",
            "source_type": "translation_memory",
            "authority": "unknown",
            "sentence_id": sentence_id,
            "document_id": record.get("document_id"),
        }

        chunks.append(source_chunk)
        chunks.append(target_chunk)

    return chunks


def create_parallel_chunks(records: list[dict]) -> list[dict]:
    """
    Create source-reference parallel sentence chunks.
    """

    chunks = []

    for record in records:

        sentence_id = str(record["id"])

        chunk = {
            "chunk_id": f"parallel_{sentence_id}",
            "source_text": record["source"],
            "target_text": record["reference"],
            "source_language": record["source_lang"],
            "target_language": record["target_lang"],
            "domain": record["domain"],
            "chunk_type": "parallel_sentence",
            "source_type": "translation_memory",
            "authority": "unknown",
            "sentence_id": sentence_id,
            "document_id": record.get("document_id"),
        }

        chunks.append(chunk)

    return chunks