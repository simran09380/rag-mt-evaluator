from models.nlp_models import nlp_en, nlp_hi
def extract_english_terminology(text: str) -> list[dict]:
    """
    Extract English terminology using spaCy noun chunks.
    """

    if not text.strip():
        return []

    doc = nlp_en(text)

    terminology = []

    seen = set()

    for chunk in doc.noun_chunks:

        # Remove determiners like "the", "a", "an"
        words = []

        for token in chunk:

            if token.pos_ != "DET":
                words.append(token.text)

        phrase = " ".join(words).strip()

        if phrase and phrase not in seen:

            seen.add(phrase)

            terminology.append(
                {
                    "term": phrase
                }
            )

    return terminology
def extract_hindi_terminology(text: str) -> list[dict]:
    """
    Extract Hindi terminology using POS tags.
    Baseline implementation.
    """

    if not text.strip():
        return []

    doc = nlp_hi(text)

    terminology = []
    seen = set()

    VALID_POS = {
        "NOUN",
        "PROPN",
        "ADJ"
    }

    IGNORE_WORDS = {
        "दिन",
        "बार",
        "समय",
        "वर्ष",
        "महीना",
        "आज",
        "कल",
        "को",
        "में",
        "से",
        "पर",
        "का",
        "की",
        "के"
    }

    for sentence in doc.sentences:

        for word in sentence.words:

            if (
                word.upos in VALID_POS
                and word.text not in IGNORE_WORDS
            ):

                if word.text not in seen:

                    seen.add(word.text)

                    terminology.append(
                        {
                            "term": word.text
                        }
                    )

    return terminology
def extract_terminology(
    text: str,
    language: str
):
    """
    Extract terminology based on language.
    """

    if language == "en":
        return extract_english_terminology(text)

    elif language == "hi":
        return extract_hindi_terminology(text)

    return []
if __name__ == "__main__":

    english = """
    The Reserve Bank of India increased the repo rate.
    """

    print(extract_terminology(
        english,
        "en"
    ))