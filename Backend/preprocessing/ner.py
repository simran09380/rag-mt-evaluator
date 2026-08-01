from models.nlp_models import nlp_en, nlp_hi


def extract_english_entities(sentences: list[str]) -> list[list[dict]]:
    """
    Extract named entities from English sentences.
    """

    if not sentences:
        return []

    entities = []

    for sentence in sentences:

        doc = nlp_en(sentence)

        sentence_entities = []

        for entity in doc.ents:

            sentence_entities.append(
                {
                    "entity": entity.text,
                    "label": entity.label_
                }
            )

        entities.append(sentence_entities)

    return entities


def extract_hindi_entities(sentences: list[str]) -> list[list[dict]]:
    """
    Extract named entities from Hindi sentences.
    """

    if not sentences:
        return []

    entities = []

    for sentence in sentences:

        doc = nlp_hi(sentence)

        sentence_entities = []

        for entity in doc.entities:

            sentence_entities.append(
                {
                    "entity": entity.text,
                    "label": entity.type
                }
            )

        entities.append(sentence_entities)

    return entities


def extract_entities(sentences: list[str], language: str):
    """
    Extract named entities based on language.
    """

    if language == "en":
        return extract_english_entities(sentences)

    elif language == "hi":
        return extract_hindi_entities(sentences)

    return []