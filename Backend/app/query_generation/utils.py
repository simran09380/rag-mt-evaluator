from models.nlp_models import nlp_en


def extract_english_terminology(text: str) -> list[str]:
    """
    Extract terminology candidates from an English sentence
    using spaCy noun chunks.
    """

    if not text.strip():
        return []

    doc = nlp_en(text)

    terminology = []
    seen = set()

    for chunk in doc.noun_chunks:

        term = chunk.text.strip().lower()

        if not term:
            continue

        if term not in seen:
            terminology.append(term)
            seen.add(term)

    return terminology