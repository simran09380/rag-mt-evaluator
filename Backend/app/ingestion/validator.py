from fastapi import HTTPException


TRANSLATION_REQUIRED_COLUMNS = {
    "source",
    "hypothesis",
    "reference"
}

PARAGRAPH_REQUIRED_COLUMNS = {
    "paragraph_id",
    "text",
    "language",
    "domain",
    "source_type",
    "authority",
    "document_id"
}
SECTION_REQUIRED_COLUMNS = {
    "section_id",
    "section_title",
    "text",
    "language",
    "domain",
    "source_type",
    "authority",
    "document_id"
}



def detect_dataset_type(records: list[dict]) -> str:
    """
    Detect whether the uploaded dataset is a
    translation dataset or a paragraph/domain document.
    """

    if not records:
        raise HTTPException(
            status_code=400,
            detail="Dataset is empty."
        )

    columns = set(records[0].keys())

    if TRANSLATION_REQUIRED_COLUMNS.issubset(columns):
        return "translation"

    if PARAGRAPH_REQUIRED_COLUMNS.issubset(columns):
        return "paragraph"

    if SECTION_REQUIRED_COLUMNS.issubset(columns):
        return "section"

    raise HTTPException(
        status_code=400,
        detail=(
            "Unsupported dataset structure. "
            "Expected either translation columns "
            "(source, hypothesis, reference) or "
            "paragraph document columns "
            "(paragraph_id, text, language, domain, "
            "source_type, authority, document_id)."
        )
    )


def validate_dataset(records: list[dict]) -> list[dict]:
    """
    Validate the loaded dataset.

    Supports:
        - translation datasets
        - paragraph/domain documents
    """

    dataset_type = detect_dataset_type(records)

    if dataset_type == "translation":
        return validate_translation_dataset(records)

    if dataset_type == "paragraph":
        return validate_paragraph_dataset(records)

    return records


def validate_translation_dataset(
    records: list[dict]
) -> list[dict]:

    seen_ids = set()
    seen_pairs = set()

    for index, record in enumerate(records, start=1):

        missing = (
            TRANSLATION_REQUIRED_COLUMNS
            - record.keys()
        )

        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Row {index}: Missing columns {missing}"
            )

        # Empty values
        for column in TRANSLATION_REQUIRED_COLUMNS:

            value = str(record[column]).strip()

            if value == "":
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Row {index}: "
                        f"'{column}' cannot be empty."
                    )
                )

        # Duplicate ID
        record_id = record.get("id")

        if record_id in seen_ids:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Row {index}: "
                    f"Duplicate ID '{record_id}'."
                )
            )

        seen_ids.add(record_id)

        # Duplicate translation pair
        pair = (
            record["source"].strip(),
            record["hypothesis"].strip()
        )

        if pair in seen_pairs:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Row {index}: "
                    "Duplicate translation pair found."
                )
            )

        seen_pairs.add(pair)

    return records


def validate_paragraph_dataset(
    records: list[dict]
) -> list[dict]:

    seen_ids = set()

    for index, record in enumerate(records, start=1):

        missing = (
            PARAGRAPH_REQUIRED_COLUMNS
            - record.keys()
        )

        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Row {index}: Missing columns {missing}"
            )

        # Empty values
        for column in PARAGRAPH_REQUIRED_COLUMNS:

            value = str(record[column]).strip()

            if value == "":
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Row {index}: "
                        f"'{column}' cannot be empty."
                    )
                )

        # Duplicate paragraph ID
        paragraph_id = record["paragraph_id"]

        if paragraph_id in seen_ids:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Row {index}: "
                    f"Duplicate paragraph_id "
                    f"'{paragraph_id}'."
                )
            )

        seen_ids.add(paragraph_id)

    return records