from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form

from app.services.evaluation_pipeline import evaluate

router = APIRouter(
    prefix="/evaluate",
    tags=["Evaluation"]
)


@router.post("/")
async def evaluate_translation(

    file: Optional[UploadFile] = File(None),

    source: Optional[str] = Form(None),
    hypothesis: Optional[str] = Form(None),
    reference: Optional[str] = Form(None),

    source_lang: Optional[str] = Form(None),
    target_lang: Optional[str] = Form(None),
    domain: Optional[str] = Form(None),
):

    return await evaluate(
        file=file,
        source=source,
        hypothesis=hypothesis,
        reference=reference,
        source_lang=source_lang,
        target_lang=target_lang,
        domain=domain,
    )