from langdetect import detect


def detect_language(text: str) -> str:
    """
    Detects the language of the given text.
    Returns language code like 'en', 'hi', etc.
    """

    return detect(text)
