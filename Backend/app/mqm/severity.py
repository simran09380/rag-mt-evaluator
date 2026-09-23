from app.mqm.taxonomy import SEVERITY_PENALTIES


def get_penalty(severity: str) -> int:
    """
    Return the MQM penalty associated with a severity level.
    """

    if severity not in SEVERITY_PENALTIES:
        raise ValueError(
            f"Invalid severity: {severity}. "
            f"Valid values are: {list(SEVERITY_PENALTIES.keys())}"
        )

    return SEVERITY_PENALTIES[severity]


def calculate_total_penalty(errors: list) -> int:
    """
    Calculate total MQM penalty from a list of errors.
    """

    return sum(
        get_penalty(error.severity.value)
        for error in errors
    )