from models.embedding_models import multilingual_model


def generate_cross_lingual_query(
    source_text: str,
    mt_output: str
) -> dict[str, list[float]]:
    """
    Generate multilingual embeddings for the
    source sentence and MT output.
    """

    if not source_text.strip() or not mt_output.strip():
        return {
            "source_embedding": [],
            "target_embedding": []
        }

    source_embedding = multilingual_model.encode(
        source_text,
        convert_to_numpy=True
    )

    target_embedding = multilingual_model.encode(
        mt_output,
        convert_to_numpy=True
    )

    return {
        "source_embedding": source_embedding.tolist(),
        "target_embedding": target_embedding.tolist()
    }