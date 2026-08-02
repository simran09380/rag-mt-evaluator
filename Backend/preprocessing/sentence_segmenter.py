from models.nlp_models import nlp_en, nlp_hi
print("File Loaded")


def segment_english(text: str) -> list[str]:
    """
    Segment English text into individual sentences.
    """

    if not text.strip():
        return []

    doc = nlp_en(text)

    sentences = []

    for sent in doc.sents:
        sentences.append(str(sent))

    return sentences


def segment_hindi(text: str) -> list[str]:
    """
    Segment Hindi text into individual sentences.
    """

    if not text.strip():
        return []

    doc = nlp_hi(text)

    sentences = []

    for sent in doc.sentences:
        sentences.append(sent.text)

    return sentences


def segment_text(text: str, language: str) -> list[str]:
    """
    Segment text based on detected language.
    """

    if language == "en":
        return segment_english(text)

    elif language == "hi":
        return segment_hindi(text)

    return [text]
if __name__ == "__main__":
    print("Main Started")

    english = "The patient has fever. He should take medicine twice daily."

    hindi = "रोगी को बुखार है। उसे दिन में दो बार दवा लेनी चाहिए।"

    print("English:")
    print(segment_text(english, "en"))

    print()

    print("Hindi:")
    print(segment_text(hindi, "hi"))