from app.query_generation.utils import extract_english_terminology


def generate_terminology_query(
    text: str,
    domain: str,
    source_lang: str,
    target_lang: str
) -> str:
    """
    Generate a terminology-focused retrieval query.
    """

    if not text.strip():
        return ""

    terminology = extract_english_terminology(text)

    if not terminology:
        return ""

    return " ".join(
        terminology + [domain, source_lang, target_lang]
    )