from .chunk_metadata import create_chunk_metadata


def create_section_chunks(sections: list[dict]) -> list[dict]:
    """
    Convert structured document sections into section-level chunks.
    """

    chunks = []

    for index, section in enumerate(sections, start=1):
        chunk_id = f"section_{index:06d}"

        chunk = create_chunk_metadata(
            chunk_id=chunk_id,
            text=section["text"],
            language=section["language"],
            domain=section["domain"],
            chunk_type="section",
            source_type=section.get(
                "source_type",
                "structured_document"
            ),
            authority=section.get(
                "authority",
                "unknown"
            ),
            document_id=section.get("document_id"),
        )

        chunk["section_title"] = section.get("section_title")
        chunk["section_number"] = section.get("section_number")

        chunks.append(chunk)

    return chunks