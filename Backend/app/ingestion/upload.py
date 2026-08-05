import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Supported file extensions
ALLOWED_EXTENSIONS = {
    ".csv",
    ".txt",
    ".jsonl",
    ".xlsx",
    ".tmx",
}


def validate_file(file: UploadFile) -> dict:
    """
    Validate the uploaded dataset file.

    Checks:
    - File is provided
    - File has a supported extension

    Returns:
        Dictionary containing file information.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded."
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type '{extension}'. "
                f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            ),
        )

    return {
        "filename": file.filename,
        "extension": extension,
        "content_type": file.content_type,
    }

def save_uploaded_file(file: UploadFile) -> Path:
    """
    Save uploaded file to uploads/ directory.

    Returns:
        Path to saved file.
    """

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path