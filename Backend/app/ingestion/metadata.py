from datetime import datetime
from pathlib import Path


def generate_metadata(
    file_info: dict,
    encoding_info: dict,
    records: list[dict]
) -> dict:
    """
    Generate metadata for the uploaded dataset.
    """

    metadata = {
        "filename": file_info["filename"],
        "file_type": Path(file_info["filename"]).suffix,
        "content_type": file_info["content_type"],
        "encoding": encoding_info["encoding"],
        "encoding_confidence": encoding_info["confidence"],
        "uploaded_at": datetime.now().isoformat(),
        "num_records": len(records)
    }

    # Optional dataset-level metadata
    if records:
        first_record = records[0]

        metadata["source_lang"] = first_record.get("source_lang")
        metadata["target_lang"] = first_record.get("target_lang")
        metadata["domain"] = first_record.get("domain")

    return metadata