from models.nlp_models import nlp_en, nlp_hi

def tag_english(sentences: list[str]) -> list[list[dict]]:
    """
    Perform POS tagging for English sentences.
    """

    if not sentences:
        return []

    pos_tags = []

    for sentence in sentences:

        doc = nlp_en(sentence)

        sentence_tags = []

        for token in doc:

            sentence_tags.append(
                {
                    "token": token.text,
                    "pos": token.pos_
                }
            )

        pos_tags.append(sentence_tags)

    return pos_tags
def tag_hindi(sentences: list[str]) -> list[list[dict]]:
    """
    Perform POS tagging for Hindi sentences.
    """

    if not sentences:
        return []

    pos_tags = []

    for sentence in sentences:

        doc = nlp_hi(sentence)

        sentence_tags = []

        for sent in doc.sentences:

            for word in sent.words:

                sentence_tags.append(
                    {
                        "token": word.text,
                        "pos": word.upos
                    }
                )

        pos_tags.append(sentence_tags)

    return pos_tags
def tag_text(sentences: list[str], language: str):
    """
    Perform POS tagging based on language.
    """

    if language == "en":
        return tag_english(sentences)

    elif language == "hi":
        return tag_hindi(sentences)

    return []