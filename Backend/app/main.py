from fastapi import FastAPI

from app.routes.query import router as query_router
from app.routes.evaluate import router as evaluate_router

app = FastAPI(
    title="RAG MT Evaluator",
    version="1.0"
)

app.include_router(evaluate_router)
app.include_router(query_router)