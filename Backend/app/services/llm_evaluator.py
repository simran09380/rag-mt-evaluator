import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from app.prompts.evaluation_prompt import build_evaluation_prompt
from app.schemas.llm_evaluation import LLMEvaluationResult
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class LLMEvaluator:
    """
    Evidence-grounded LLM evaluator using Google Gemini.
    """

    def __init__(
        self,
        model: str = "gemini-3.5-flash-lite",
    ):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set in the environment."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def evaluate(
        self,
        source: str,
        translation: str,
        source_lang: str,
        target_lang: str,
        domain: Optional[str] = None,
        reference: Optional[str] = None,
        evidence: Optional[list] = None,
        metrics: Optional[dict] = None,
        evaluation_instructions: Optional[str] = None,
    ) -> dict:

        # ----------------------------------------------------
        # 1. Build evidence-grounded prompt
        # ----------------------------------------------------

        prompt = build_evaluation_prompt(
            source=source,
            translation=translation,
            source_lang=source_lang,
            target_lang=target_lang,
            domain=domain,
            reference=reference,
            evidence=evidence,
            metrics=metrics,
            evaluation_instructions=evaluation_instructions,
        )

        # ----------------------------------------------------
        # 2. Ask Gemini for structured JSON
        # ----------------------------------------------------

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=LLMEvaluationResult,
            ),
        )

        # ----------------------------------------------------
        # 3. Check response
        # ----------------------------------------------------

        if not response.text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        # ----------------------------------------------------
        # 4. Validate Gemini response
        # ----------------------------------------------------

        try:
            validated_result = (
                LLMEvaluationResult.model_validate_json(
                    response.text
                )
            )

        except ValidationError as exc:
            raise ValueError(
                f"Gemini response failed schema validation: {exc}"
            ) from exc

        # ----------------------------------------------------
        # 5. Validate evidence IDs
        # ----------------------------------------------------

        valid_evidence_ids = {
            item.get("id")
            for item in (evidence or [])
            if item.get("id")
        }

        result_data = validated_result.model_dump()

        for dimension_name, judgment in result_data.items():

            evidence_ids = judgment.get(
                "evidence_ids",
                []
            )

            invalid_ids = [
                evidence_id
                for evidence_id in evidence_ids
                if evidence_id not in valid_evidence_ids
            ]

            if invalid_ids:
                raise ValueError(
                    f"{dimension_name} contains invalid "
                    f"evidence IDs: {invalid_ids}"
                )

        # ----------------------------------------------------
        # 6. Return final Module 8 result
        # ----------------------------------------------------

        return {
            "evaluation": result_data,
            "model": self.model,
            "supported_by_evidence": True,
        }