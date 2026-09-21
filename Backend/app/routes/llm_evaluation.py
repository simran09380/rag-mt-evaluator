from fastapi import APIRouter

from app.schemas.llm_evaluation import LLMEvaluationRequest
from app.services.llm_evaluator import LLMEvaluator


router = APIRouter(
    prefix="/evaluate/llm",
    tags=["LLM Evaluation"]
)


@router.post("/")
async def evaluate_with_llm(request: LLMEvaluationRequest):

    evaluator = LLMEvaluator()

    result = evaluator.evaluate(
        source=request.source,
        translation=request.translation,
        source_lang=request.source_lang,
        target_lang=request.target_lang,
        domain=request.domain,
        reference=request.reference,
        evidence=[
            item.model_dump()
            for item in request.retrieved_evidence.evidence
        ],
        metrics=(
            request.metrics.model_dump()
            if request.metrics
            else None
        ),
        evaluation_instructions=request.evaluation_instructions,
    )

    return result