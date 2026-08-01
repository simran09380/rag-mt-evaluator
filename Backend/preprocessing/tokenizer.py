from models.nlp_models import nlp_en, nlp_hi


def tokenize_english(sentences: list[str]) -> list[list[str]]:
    """
    Tokenize English sentences.
    """

    if not sentences:
        return []

    tokens = []

    for sentence in sentences:

        doc = nlp_en(sentence)

        sentence_tokens = []

        for token in doc:
            sentence_tokens.append(token.text)

        tokens.append(sentence_tokens)

    return tokens


def tokenize_hindi(sentences: list[str]) -> list[list[str]]:
    """
    Tokenize Hindi sentences.
    """

    if not sentences:
        return []

    tokens = []

    for sentence in sentences:

        doc = nlp_hi(sentence)

        sentence_tokens = []

        for sent in doc.sentences:
            for word in sent.words:
                sentence_tokens.append(word.text)

        tokens.append(sentence_tokens)

    return tokens


def tokenize_text(sentences: list[str], language: str) -> list[list[str]]:
    """
    Tokenize text based on language.
    """

    if language == "en":
        return tokenize_english(sentences)

    elif language == "hi":
        return tokenize_hindi(sentences)

    return []