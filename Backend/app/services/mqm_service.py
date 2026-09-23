import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from app.mqm.classifier import (
    classify_error,
    build_mqm_evaluation,
)
from app.mqm.taxonomy import MQM_TAXONOMY
from app.prompts.mqm_prompt import build_mqm_prompt
from app.schemas.mqm_llm import MQMClassificationResult


load_dotenv()


class MQMService:
    """
    MQM error classifier using Google Gemini.
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

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = model

    def classify(
        self,
        source: str,
        translation: str,
        source_lang: str,
        target_lang: str,
        domain: str | None = None,
        reference: str | None = None,
        evidence: list | None = None,
        llm_evaluation: dict | None = None,
    ) -> dict[str, Any]:

        prompt = build_mqm_prompt(
            source=source,
            translation=translation,
            source_lang=source_lang,
            target_lang=target_lang,
            domain=domain,
            reference=reference,
            evidence=evidence,
            llm_evaluation=llm_evaluation or {},
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=MQMClassificationResult,
            ),
        )

        if not response.text:
            raise ValueError(
                "Gemini returned an empty MQM response."
            )

        try:
            validated_result = (
                MQMClassificationResult.model_validate_json(
                    response.text
                )
            )

        except ValidationError as exc:
            raise ValueError(
                f"MQM response failed schema validation: {exc}"
            ) from exc

        valid_evidence_ids = {
            item.get("id")
            for item in (evidence or [])
            if item.get("id")
        }

        mqm_errors = []

        for error in validated_result.errors:

            category = error.category.value
            error_type = error.error_type
            severity = error.severity.value

            # --------------------------------------------
            # Validate MQM taxonomy
            # --------------------------------------------

            if category not in MQM_TAXONOMY:
                raise ValueError(
                    f"Invalid MQM category: {category}"
                )

            if error_type not in MQM_TAXONOMY[category]:
                raise ValueError(
                    f"Invalid MQM error type '{error_type}' "
                    f"for category '{category}'."
                )

            # --------------------------------------------
            # Validate evidence
            # --------------------------------------------

            invalid_ids = [
                evidence_id
                for evidence_id in error.evidence_ids
                if evidence_id not in valid_evidence_ids
            ]

            if invalid_ids:
                raise ValueError(
                    f"MQM error contains invalid evidence IDs: "
                    f"{invalid_ids}"
                )

            # --------------------------------------------
            # Build validated MQM error
            # --------------------------------------------

            mqm_error = classify_error(
                category=category,
                error_type=error_type,
                severity=severity,
                description=error.description,
                evidence_ids=error.evidence_ids,
            )

            mqm_errors.append(mqm_error)

        return build_mqm_evaluation(mqm_errors)