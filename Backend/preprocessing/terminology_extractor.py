import yake

from models.nlp_models import nlp_en, nlp_hi

# Load YAKE extractor only once
extractor_en = yake.KeywordExtractor(lan="en")
extractor_hi = yake.KeywordExtractor(lan="hi")

# Valid POS tags for terminology
VALID_POS = {
    "NOUN",
    "PROPN",
    "ADJ"
}


def filter_terms_by_pos(text: str, language: str) -> set[str]:
    """
    Filter extracted keywords using POS tags.
    """

    terms = set()

    if language == "en":

        doc = nlp_en(text)

        for token in doc:

            if token.pos_ in VALID_POS:
                terms.add(token.text)

    elif language == "hi":

        doc = nlp_hi(text)

        for sentence in doc.sentences:

            for word in sentence.words:

                if word.upos in VALID_POS:
                    terms.add(word.text)

    return terms


def extract_terminology(text: str, language: str) -> list[dict]:
    """
    Extract important terminology using YAKE and POS filtering.
    """

    if not text.strip():
        return []

    if language == "en":
        keywords = extractor_en.extract_keywords(text)

    elif language == "hi":
        keywords = extractor_hi.extract_keywords(text)

    else:
        return []

    terms = {}

    for keyword, score in keywords:

        filtered_terms = filter_terms_by_pos(
            keyword,
            language
        )

        for term in filtered_terms:

            # Keep the lowest YAKE score
            if term not in terms or score < terms[term]:
                terms[term] = score

    terminology = []

    for term, score in terms.items():

        terminology.append(
            {
                "term": term,
                "score": score
            }
        )

    return terminology