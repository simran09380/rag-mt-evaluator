from models.nlp_models import nlp_en, nlp_hi


def parse_english(sentences: list[str]) -> list[list[dict]]:
    """
    Perform dependency parsing for English sentences.
    """

    if not sentences:
        return []

    dependencies = []

    for sentence in sentences:

        doc = nlp_en(sentence)

        sentence_dependencies = []

        for token in doc:

            sentence_dependencies.append(
                {
                    "token": token.text,
                    "pos": token.pos_,
                    "dependency": token.dep_,
                    "head": token.head.text
                }
            )

        dependencies.append(sentence_dependencies)

    return dependencies


def parse_hindi(sentences: list[str]) -> list[list[dict]]:
    """
    Perform dependency parsing for Hindi sentences.
    """

    if not sentences:
        return []

    dependencies = []

    for sentence in sentences:

        doc = nlp_hi(sentence)

        sentence_dependencies = []

        for sent in doc.sentences:

            words = sent.words

            for word in words:

                if word.head == 0:
                    head = "ROOT"
                else:
                    head = words[word.head - 1].text

                sentence_dependencies.append(
                    {
                        "token": word.text,
                        "pos": word.upos,
                        "dependency": word.deprel,
                        "head": head
                    }
                )

        dependencies.append(sentence_dependencies)

    return dependencies


def parse_text(sentences: list[str], language: str):
    """
    Perform dependency parsing based on language.
    """

    if language == "en":
        return parse_english(sentences)

    elif language == "hi":
        return parse_hindi(sentences)

    return []