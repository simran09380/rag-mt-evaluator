import re
import unicodedata


TEXT_FIELDS = [
    "source",
    "hypothesis",
    "reference"
]


def clean_dataset(records: list[dict]) -> list[dict]:
    """
    Clean the dataset.

    Operations:
    - Remove leading/trailing spaces
    - Collapse multiple spaces
    - Normalize Unicode
    """

    cleaned_records = []

    for record in records:

        cleaned = record.copy()

        for field in TEXT_FIELDS:

            if field in cleaned:

                value = str(cleaned[field])

                # Unicode normalization
                value = unicodedata.normalize("NFC", value)

                # Remove leading/trailing spaces
                value = value.strip()

                # Replace multiple spaces with one
                value = re.sub(r"\s+", " ", value)

                cleaned[field] = value

        cleaned_records.append(cleaned)

    return cleaned_records