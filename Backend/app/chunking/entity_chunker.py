from .chunk_metadata import create_chunk_metadata


def create_entity_chunks(entities: list[dict]) -> list[dict]:
    """
    Convert named entities from Module 2
    into entity-level chunks.
    """

    chunks = []

    for index, entity in enumerate(entities, start=1):

        chunk_id = f"entity_{index:06d}"

        chunk = create_chunk_metadata(
            chunk_id=chunk_id,
            text=entity["entity"],
            language=entity["language"],
            domain=entity["domain"],
            chunk_type="named_entity",
            source_type=entity.get(
                "source_type",
                "named_entity_extraction"
            ),
            authority=entity.get(
                "authority",
                "unknown"
            ),
            document_id=entity.get("document_id"),
        )

        chunk["entity_type"] = entity.get("label")

        chunks.append(chunk)

    return chunks