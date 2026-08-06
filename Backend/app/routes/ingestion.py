from fastapi import APIRouter, UploadFile, File
from app.ingestion.pipeline import ingest_dataset

router = APIRouter(
    prefix="/ingestion",
    tags=["Data Ingestion"]
)


@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    return ingest_dataset(file)