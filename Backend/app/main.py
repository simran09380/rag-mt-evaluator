from fastapi import FastAPI

from app.routes.query import router as query_router
from app.routes.evaluate import router as evaluate_router
from app.routes.llm_evaluation import router as llm_evaluation_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RAG MT Evaluator",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(evaluate_router)
app.include_router(query_router)
app.include_router(llm_evaluation_router)