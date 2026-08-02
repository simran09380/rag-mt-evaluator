from models.nlp_models import ner_model, nlp_hi


# Labels for English GLiNER
LABELS = [
    "PERSON",
    "ORGANIZATION",
    "LOCATION",
    "DATE",
    "TIME",
    "PRODUCT",
    "EVENT",
    "DISEASE"
]


def extract_entities(
    text: str,
    language: str
) -> list[dict]:
    """
    Extract named entities.

    English -> GLiNER
    Hindi -> Stanza
    """

    if not text.strip():
        return []

    entities = []
    seen = set()

    # --------------------------
    # English
    # --------------------------

    if language == "en":

        predictions = ner_model.predict_entities(
            text,
            LABELS
        )

        for prediction in predictions:

            entity = prediction["text"].strip()
            label = prediction["label"]

            # Remove leading articles
            for article in ("The ", "the ", "A ", "An "):

                if entity.startswith(article):
                    entity = entity[len(article):]

            key = (entity, label)

            if key in seen:
                continue

            seen.add(key)

            entities.append(
                {
                    "entity": entity,
                    "label": label
                }
            )

    # --------------------------
    # Hindi
    # --------------------------

    elif language == "hi":

        doc = nlp_hi(text)

        for sentence in doc.sentences:

            for ent in sentence.ents:

                entity = ent.text.strip()
                label = ent.type

                key = (entity, label)

                if key in seen:
                    continue

                seen.add(key)

                entities.append(
                    {
                        "entity": entity,
                        "label": label
                    }
                )

    return entities


