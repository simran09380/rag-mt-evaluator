# import yake

# from models.nlp_models import nlp_en, nlp_hi

# # -----------------------------
# # YAKE Extractors
# # -----------------------------
# extractor_en = yake.KeywordExtractor(lan="en")
# extractor_hi = yake.KeywordExtractor(lan="hi")

# # -----------------------------
# # POS Configuration
# # -----------------------------
# VALID_POS = {
#     "NOUN",
#     "PROPN",
#     "ADJ"
# }

# CONNECTOR_POS = {
#     "ADP",
#     "CCONJ"
# }

# VERB_POS = {
#     "VERB",
#     "AUX"
# }


# def filter_terms_by_pos(text: str, language: str) -> list[str]:
#     """
#     Preserve complete terminology phrases whenever possible.
#     Split only when verbs are present.
#     """

#     # ------------------ English ------------------

#     if language == "en":

#         doc = nlp_en(text)

#         has_verb = any(
#             token.pos_ in VERB_POS
#             for token in doc
#         )

#         # Example:
#         # patient has fever
#         if has_verb:

#             terms = []

#             for token in doc:

#                 if token.pos_ in VALID_POS:
#                     terms.append(token.text)

#             return terms

#         # Example:
#         # Reserve Bank of India
#         phrase = []

#         for token in doc:

#             if (
#                 token.pos_ in VALID_POS
#                 or token.pos_ in CONNECTOR_POS
#             ):
#                 phrase.append(token.text)

#         if phrase:
#             return [" ".join(phrase)]

#         return []

#     # ------------------ Hindi ------------------

#     elif language == "hi":

#         doc = nlp_hi(text)

#         has_verb = any(
#             word.upos in VERB_POS
#             for sent in doc.sentences
#             for word in sent.words
#         )

#         if has_verb:

#             terms = []

#             for sent in doc.sentences:

#                 for word in sent.words:

#                     if word.upos in VALID_POS:
#                         terms.append(word.text)

#             return terms

#         phrase = []

#         for sent in doc.sentences:

#             for word in sent.words:

#                 if (
#                     word.upos in VALID_POS
#                     or word.upos in CONNECTOR_POS
#                 ):
#                     phrase.append(word.text)

#         if phrase:
#             return [" ".join(phrase)]

#         return []

#     return []


# def extract_terminology(text: str, language: str) -> list[dict]:
#     """
#     Extract terminology using YAKE and POS filtering.
#     """

#     if not text.strip():
#         return []

#     # -----------------------------
#     # Select Extractor
#     # -----------------------------

#     if language == "en":
#         keywords = extractor_en.extract_keywords(text)

#     elif language == "hi":
#         keywords = extractor_hi.extract_keywords(text)

#     else:
#         return []

#     terms = {}

#     # -----------------------------
#     # Process YAKE Keywords
#     # -----------------------------

#     for keyword, score in keywords:

#         filtered_terms = filter_terms_by_pos(
#             keyword,
#             language
#         )

#         for term in filtered_terms:

#             term = term.strip()

#             if not term:
#                 continue

#             # Keep best YAKE score
#             if term not in terms or score < terms[term]:
#                 terms[term] = score

#     terminology = []

#     # Sort by score (lower = better)
#     for term, score in sorted(
#         terms.items(),
#         key=lambda x: x[1]
#     ):

#         terminology.append(
#             {
#                 "term": term,
#                 "score": score
#             }
#         )

#     return terminology


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