from fastapi import FastAPI
from app.schemas import TranslationRequest
from pipeline.preprocessing_pipeline import preprocess
from app.routes.ingestion import router as ingestion_router

app = FastAPI(
    title="RAG MT Evaluator",
    version="1.0"
)

app.include_router(ingestion_router)

@app.post("/evaluate")
def evaluate(data: TranslationRequest):
    processed = preprocess(
    data.source,
    data.hypothesis
    )
    return processed
    