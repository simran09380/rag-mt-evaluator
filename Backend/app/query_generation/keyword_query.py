from models.nlp_models import nlp_en


def generate_keyword_query(text: str) -> str:
    """
    Generate a keyword-based retrieval query
    from the source sentence.
    """

    if not text.strip():
        return ""

    doc = nlp_en(text)

    keywords = []

    for token in doc:

        if token.is_stop:
            continue

        if token.is_punct:
            continue

        if token.pos_ not in {"NOUN", "PROPN", "VERB", "ADJ"}:
            continue

        keywords.append(token.lemma_.lower())

    return " ".join(dict.fromkeys(keywords))