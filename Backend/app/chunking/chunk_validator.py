ALLOWED_CHUNK_TYPES = {
    "sentence",
    "term",
    "paragraph",
    "section",
    "parallel_sentence",
    "named_entity"
}

REQUIRED_FIELDS = {
    "chunk_id",
    "text",
    "language",
    "domain",
    "chunk_type",
    "source_type",
    "authority"
}


def validate_parallel_chunk(chunk: dict) -> tuple[bool, list[str]]:
    """
    Validate a parallel source-reference chunk.
    """

    errors = []

    required_fields = {
        "chunk_id",
        "source_text",
        "target_text",
        "source_language",
        "target_language",
        "domain",
        "chunk_type",
        "source_type",
        "authority"
    }

    for field in required_fields:
        if field not in chunk:
            errors.append(
                f"Missing required field: {field}"
            )

    if errors:
        return False, errors

    if not isinstance(chunk["source_text"], str):
        errors.append("Source text must be a string")
    elif not chunk["source_text"].strip():
        errors.append("Source text cannot be empty")

    if not isinstance(chunk["target_text"], str):
        errors.append("Target text must be a string")
    elif not chunk["target_text"].strip():
        errors.append("Target text cannot be empty")

    if chunk["chunk_type"] != "parallel_sentence":
        errors.append(
            "Invalid chunk type for parallel chunk"
        )

    return len(errors) == 0, errors


def validate_chunk(chunk: dict) -> tuple[bool, list[str]]:
    """
    Validate a single chunk.
    """

    # Parallel chunks have a different structure
    if chunk.get("chunk_type") == "parallel_sentence":
        return validate_parallel_chunk(chunk)

    errors = []

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in chunk:
            errors.append(
                f"Missing required field: {field}"
            )

    if errors:
        return False, errors

    # Empty values
    for field in REQUIRED_FIELDS:
        value = chunk.get(field)

        if value is None:
            errors.append(
                f"Empty value for field: {field}"
            )

        elif isinstance(value, str) and not value.strip():
            errors.append(
                f"Empty value for field: {field}"
            )

    # Chunk type
    if chunk["chunk_type"] not in ALLOWED_CHUNK_TYPES:
        errors.append(
            f"Invalid chunk type: {chunk['chunk_type']}"
        )

    # Text
    if not isinstance(chunk["text"], str):
        errors.append("Text must be a string")

    elif not chunk["text"].strip():
        errors.append("Text cannot be empty")

    return len(errors) == 0, errors


def validate_chunks(chunks: list[dict]) -> dict:
    """
    Validate a collection of chunks.

    Returns valid and invalid chunks separately.
    """

    valid_chunks = []
    invalid_chunks = []
    errors = []

    seen_chunk_ids = set()

    for chunk in chunks:

        chunk_id = chunk.get("chunk_id")

        # Duplicate chunk ID
        if chunk_id in seen_chunk_ids:

            invalid_chunks.append(chunk)

            errors.append({
                "chunk_id": chunk_id,
                "errors": ["Duplicate chunk_id"]
            })

            continue

        seen_chunk_ids.add(chunk_id)

        # Validate individual chunk
        is_valid, chunk_errors = validate_chunk(chunk)

        if is_valid:
            valid_chunks.append(chunk)

        else:
            invalid_chunks.append(chunk)

            errors.append({
                "chunk_id": chunk_id,
                "errors": chunk_errors
            })

    return {
        "valid_chunks": valid_chunks,
        "invalid_chunks": invalid_chunks,
        "errors": errors
    }