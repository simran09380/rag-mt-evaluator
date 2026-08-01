from fastapi import FastAPI
from app.schemas import TranslationRequest
from pipeline.preprocessing_pipeline import preprocess

app = FastAPI(
    title="RAG MT Evaluator",
    version="1.0"
)


@app.post("/evaluate")
def evaluate(data: TranslationRequest):
    processed = preprocess(
    data.source,
    data.hypothesis
    )
    return processed
    