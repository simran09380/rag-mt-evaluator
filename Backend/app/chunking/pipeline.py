from .sentence_chunker import (
    create_sentence_chunks,
    create_parallel_chunks
)

from .term_chunker import create_term_chunks
from .paragraph_chunker import create_paragraph_chunks
from .section_chunker import create_section_chunks

from .chunk_validator import validate_chunks
from .entity_chunker import create_entity_chunks


def build_chunks(
    sentence_records=None,
    term_records=None,
    entity_records=None,
    paragraph_records=None,
    section_records=None
):
    """
    Build and validate all chunks for Module 4.

    Retrieval is NOT performed here.
    """

    all_chunks = []

    # Sentence chunks
    if sentence_records:
        sentence_chunks = create_sentence_chunks(
            sentence_records
        )

        parallel_chunks = create_parallel_chunks(
            sentence_records
        )

        all_chunks.extend(sentence_chunks)
        all_chunks.extend(parallel_chunks)

    # Term chunks
    if term_records:
        term_chunks = create_term_chunks(
            term_records
        )

        all_chunks.extend(term_chunks)

    # Entity chunks
    if entity_records:
        entity_chunks = create_entity_chunks(
            entity_records
        )

        all_chunks.extend(entity_chunks)

    # Paragraph chunks
    if paragraph_records:
        paragraph_chunks = create_paragraph_chunks(
            paragraph_records
        )

        all_chunks.extend(paragraph_chunks)

    # Section chunks
    if section_records:
        section_chunks = create_section_chunks(
            section_records
        )

        all_chunks.extend(section_chunks)

    # Validate everything
    validation_result = validate_chunks(
        all_chunks
    )

    return validation_result