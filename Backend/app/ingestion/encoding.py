from pathlib import Path
from charset_normalizer import from_path


def detect_encoding(file_path: str | Path) -> dict:
    """
    Detect the encoding of a text file.

    Args:
        file_path: Path to the uploaded file.

    Returns:
        Dictionary containing:
            - encoding
            - confidence
    """

    result = from_path(file_path).best()

    if result is None:
        raise ValueError("Unable to detect file encoding.")

    return {
        "encoding": result.encoding,
        "confidence": result.percent_coherence / 100
    }