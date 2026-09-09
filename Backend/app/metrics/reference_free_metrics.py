from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MULTILINGUAL_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

_similarity_model = None


def get_similarity_model():
    global _similarity_model

    if _similarity_model is None:
        _similarity_model = SentenceTransformer(MULTILINGUAL_MODEL)

    return _similarity_model


def calculate_multilingual_similarity(
    source: str,
    hypothesis: str
) -> float:
    """
    Calculate multilingual semantic similarity
    between source and hypothesis.
    """

    model = get_similarity_model()

    embeddings = model.encode(
        [source, hypothesis],
        normalize_embeddings=True
    )

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(score)

def calculate_word_alignment_coverage(
    source: str,
    hypothesis: str,
    threshold: float = 0.65
) -> float:
    """
    Calculate word-level semantic alignment coverage
    between source and hypothesis.

    For each source word, find the most similar
    hypothesis word. The score is the proportion
    of source words that have a sufficiently similar
    counterpart in the hypothesis.
    """

    model = get_similarity_model()

    source_words = source.split()
    hypothesis_words = hypothesis.split()

    if not source_words or not hypothesis_words:
        return 0.0

    source_embeddings = model.encode(
        source_words,
        normalize_embeddings=True
    )

    hypothesis_embeddings = model.encode(
        hypothesis_words,
        normalize_embeddings=True
    )

    similarity_matrix = cosine_similarity(
        source_embeddings,
        hypothesis_embeddings
    )

    aligned_words = 0

    for row in similarity_matrix:
        best_similarity = max(row)

        if best_similarity >= threshold:
            aligned_words += 1

    coverage = aligned_words / len(source_words)

    return float(coverage)

def calculate_entity_preservation(
    source: str,
    hypothesis: str
) -> float:
    """
    Calculate entity preservation between source and hypothesis.

    Entities such as names, organizations, numbers, dates,
    and other important named items are extracted from the
    source and checked for preservation in the hypothesis.
    """

    import re

    # Detect common entity-like patterns
    entity_patterns = [
        r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Names / proper nouns
        r'\b\d+(?:\.\d+)?\b',                   # Numbers
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', # Dates
        r'\b[A-Z]{2,}\b'                       # Acronyms
    ]

    source_entities = []

    for pattern in entity_patterns:
        source_entities.extend(
            re.findall(pattern, source)
        )

    # Remove duplicates while preserving order
    source_entities = list(dict.fromkeys(source_entities))

    if not source_entities:
        return 1.0

    hypothesis_lower = hypothesis.lower()

    preserved = 0

    for entity in source_entities:
        if entity.lower() in hypothesis_lower:
            preserved += 1

    return preserved / len(source_entities)


def calculate_terminology_accuracy(
    source: str,
    hypothesis: str
) -> float:
    """
    Calculate terminology accuracy between source and hypothesis.

    Important terms from the source are identified using
    noun-like words and checked for semantic preservation
    in the hypothesis.
    """

    model = get_similarity_model()

    source_terms = [
        word.strip(".,!?;:()[]{}")
        for word in source.split()
        if len(word.strip(".,!?;:()[]{}")) >= 4
    ]

    hypothesis_terms = [
        word.strip(".,!?;:()[]{}")
        for word in hypothesis.split()
        if len(word.strip(".,!?;:()[]{}")) >= 4
    ]

    if not source_terms:
        return 1.0

    if not hypothesis_terms:
        return 0.0

    source_embeddings = model.encode(
        source_terms,
        normalize_embeddings=True
    )

    hypothesis_embeddings = model.encode(
        hypothesis_terms,
        normalize_embeddings=True
    )

    similarity_matrix = cosine_similarity(
        source_embeddings,
        hypothesis_embeddings
    )

    preserved_terms = 0

    for row in similarity_matrix:
        best_similarity = max(row)

        if best_similarity >= 0.65:
            preserved_terms += 1

    accuracy = preserved_terms / len(source_terms)

    return float(accuracy)

def calculate_length_ratio(
    source: str,
    hypothesis: str
) -> float:
    """
    Calculate the length ratio between hypothesis and source.

    Length ratio = number of hypothesis tokens /
                   number of source tokens.
    """

    source_tokens = source.split()
    hypothesis_tokens = hypothesis.split()

    if not source_tokens:
        return 0.0

    return len(hypothesis_tokens) / len(source_tokens)


def calculate_untranslated_token_ratio(
    source: str,
    hypothesis: str
) -> float:
    """
    Calculate the ratio of source tokens that appear
    unchanged in the hypothesis.

    Higher values may indicate that source words were
    left untranslated.
    """

    source_tokens = [
        token.strip(".,!?;:()[]{}\"'")
        for token in source.split()
        if token.strip(".,!?;:()[]{}\"'")
    ]

    hypothesis_tokens = {
        token.strip(".,!?;:()[]{}\"'").lower()
        for token in hypothesis.split()
        if token.strip(".,!?;:()[]{}\"'")
    }

    if not source_tokens:
        return 0.0

    untranslated_tokens = 0

    for token in source_tokens:
        if token.lower() in hypothesis_tokens:
            untranslated_tokens += 1

    return float(untranslated_tokens / len(source_tokens))

