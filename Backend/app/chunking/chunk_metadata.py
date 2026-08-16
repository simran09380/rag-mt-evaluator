from typing import Optional


def create_chunk_metadata(
    chunk_id: str,
    text: str,
    language: str,
    domain: str,
    chunk_type: str,
    source_type: str,
    authority: str = "unknown",
    sentence_id: Optional[int] = None,
    document_id: Optional[str] = None,
    paired_translation: Optional[str] = None,
):
    """
    Create standardized metadata for a document chunk.
    """

    metadata = {
        "chunk_id": chunk_id,
        "text": text,
        "language": language,
        "domain": domain,
        "chunk_type": chunk_type,
        "source_type": source_type,
        "authority": authority,
    }

    if sentence_id is not None:
        metadata["sentence_id"] = sentence_id

    if document_id is not None:
        metadata["document_id"] = document_id

    if paired_translation is not None:
        metadata["paired_translation"] = paired_translation

    return metadata