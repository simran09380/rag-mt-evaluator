from app.terminology.extractor import extract_english_terminology


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

    terms = []

    for item in terminology:
        term = item.get("term")

        if term:
            terms.append(term.strip())

    terms = list(dict.fromkeys(terms))

    if not terms:
        return ""

    return " ".join(
        terms + [domain, source_lang, target_lang]
    )