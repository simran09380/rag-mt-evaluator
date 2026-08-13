from models.embedding_models import semantic_model


def generate_semantic_query(text: str) -> list[float]:
    """
    Generate a semantic embedding from the source sentence.
    """

    if not text.strip():
        return []

    embedding = semantic_model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding.tolist()