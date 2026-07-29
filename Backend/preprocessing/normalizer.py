import unicodedata


def normalize_text(text: str) -> str:
    """
    Normalize Unicode text into a standard form.
    """
    return unicodedata.normalize("NFC", text)