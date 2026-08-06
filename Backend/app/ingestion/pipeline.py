from app.ingestion.upload import (
    validate_file,
    save_uploaded_file
)
from app.ingestion.encoding import detect_encoding
from app.ingestion.readers import read_dataset
from app.ingestion.validator import validate_dataset
from app.ingestion.cleaner import clean_dataset
from app.ingestion.sentence_id import assign_sentence_ids
from app.ingestion.metadata import generate_metadata


def ingest_dataset(file):

    # Validate
    file_info = validate_file(file)

    # Save
    file_path = save_uploaded_file(file)

    # Encoding
    if file_info["extension"] != ".xlsx":
        encoding_info = detect_encoding(file_path)
    else:
        encoding_info = {
            "encoding": None,
            "confidence": None
        }

    # Read
    data = read_dataset(
        file_path=file_path,
        extension=file_info["extension"],
        encoding=encoding_info["encoding"]
    )

    # Validate
    validated_data = validate_dataset(data)

    # Clean
    cleaned_data = clean_dataset(validated_data)

    # Sentence IDs
    final_data = assign_sentence_ids(cleaned_data)

    # Metadata
    metadata = generate_metadata(
        file_info=file_info,
        encoding_info=encoding_info,
        records=final_data
    )

    return {
        "message": "File uploaded successfully.",
        "metadata": metadata,
        "data": final_data
    }