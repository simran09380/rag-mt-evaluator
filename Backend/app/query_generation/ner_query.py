from models.nlp_models import nlp_en


def generate_ner_query(
    text: str,
    target_lang: str
) -> list[str]:
    """
    Generate named-entity retrieval queries
    from the source sentence.
    """

    if not text.strip():
        return []

    doc = nlp_en(text)

    queries = []

    for entity in doc.ents:

        entity_text = entity.text.strip()

        if not entity_text:
            continue

        query = (
            f"{entity_text} "
            f"{target_lang} "
            f"official translation"
        )

        queries.append(query)

    return list(dict.fromkeys(queries))