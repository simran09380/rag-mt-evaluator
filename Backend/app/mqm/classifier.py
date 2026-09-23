from typing import Optional

from app.mqm.taxonomy import MQM_TAXONOMY, SEVERITY_PENALTIES


def validate_error_type(
    category: str,
    error_type: str
) -> bool:
    """
    Check whether an MQM error type belongs to the given category.
    """

    if category not in MQM_TAXONOMY:
        return False

    return error_type in MQM_TAXONOMY[category]


def validate_severity(severity: str) -> bool:
    """
    Check whether the severity is a valid MQM severity level.
    """

    return severity in SEVERITY_PENALTIES


def classify_error(
    category: str,
    error_type: str,
    severity: str,
    description: str,
    evidence_ids: Optional[list[str]] = None
) -> dict:
    """
    Create a validated MQM error.
    """

    if not validate_error_type(category, error_type):
        raise ValueError(
            f"Invalid MQM error type '{error_type}' "
            f"for category '{category}'."
        )

    if not validate_severity(severity):
        raise ValueError(
            f"Invalid severity '{severity}'. "
            f"Valid severities: {list(SEVERITY_PENALTIES.keys())}"
        )

    penalty = SEVERITY_PENALTIES[severity]

    return {
        "category": category,
        "error_type": error_type,
        "severity": severity,
        "penalty": penalty,
        "description": description,
        "evidence_ids": evidence_ids or [],
    }

def build_mqm_evaluation(errors: list[dict]) -> dict:
    """
    Build the final MQM evaluation from classified errors.
    """

    total_errors = len(errors)

    total_penalty = sum(
        error["penalty"]
        for error in errors
    )

    return {
        "errors": errors,
        "total_errors": total_errors,
        "total_penalty": total_penalty,
    }