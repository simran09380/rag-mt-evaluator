from fastapi import APIRouter
from pydantic import BaseModel

from app.query_generation.pipeline import generate_queries


router = APIRouter(
    prefix="/query",
    tags=["Query Generation"]
)


class QueryGenerationRequest(BaseModel):
    source_text: str
    mt_output: str
    source_lang: str
    target_lang: str
    domain: str


@router.post("/generate")
def generate_queries_endpoint(
    request: QueryGenerationRequest
):
    return generate_queries(
        source_text=request.source_text,
        mt_output=request.mt_output,
        source_lang=request.source_lang,
        target_lang=request.target_lang,
        domain=request.domain
    )