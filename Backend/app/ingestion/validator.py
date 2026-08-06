from fastapi import HTTPException


REQUIRED_COLUMNS = {
    "source",
    "hypothesis",
    "reference"
}


def validate_dataset(records: list[dict]) -> list[dict]:
    """
    Validate the loaded dataset.

    Returns:
        Validated records.
    """

    if not records:
        raise HTTPException(
            status_code=400,
            detail="Dataset is empty."
        )

    seen_ids = set()
    seen_pairs = set()
    for index, record in enumerate(records, start=1):

        #required columns
        missing = REQUIRED_COLUMNS - record.keys()

        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Row {index}: Missing columns {missing}"
            )

        #empty vlaues
        for column in REQUIRED_COLUMNS:

            value = str(record[column]).strip()

            if value == "":
                raise HTTPException(
                    status_code=400,
                    detail=f"Row {index}: '{column}' cannot be empty."
                )

        #duplicate id
        record_id = record.get("id")

        if record_id in seen_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Row {index}: Duplicate ID '{record_id}'."
            )

        seen_ids.add(record_id)

        #duplicate translation pair
        pair = (
            record["source"].strip(),
            record["hypothesis"].strip()
        )

        if pair in seen_pairs:
            raise HTTPException(
                status_code=400,
                detail=f"Row {index}: Duplicate translation pair found."
            )

        seen_pairs.add(pair)

    return records