from fastapi import APIRouter, UploadFile, File

from app.ingestion.upload import (
    validate_file,
    save_uploaded_file
)
from app.ingestion.encoding import detect_encoding

router = APIRouter(
    prefix="/ingestion",
    tags=["Data Ingestion"],
)


@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload a translation evaluation dataset.
    """

    file_info = validate_file(file)

    file_path = save_uploaded_file(file)

    # Detect Encoding
    if file_info["extension"] != ".xlsx":
        encoding_info = detect_encoding(file_path)
    else:
        encoding_info = {
            "encoding": None,
            "confidence": None
        }


    return {
        "message": "File uploaded successfully.",
        "file": file_info,
         "encoding": encoding_info
    }