from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def generate_embedding(text: str) -> list[float]:
    """
    Generate a multilingual embedding for a text.
    """

    if not text or not text.strip():
        return []

    embedding = model.encode(text)

    return embedding.tolist()


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Generate embeddings for all text-based chunks.
    """

    embedded_chunks = []

    for chunk in chunks:

        chunk = chunk.copy()

        if chunk["chunk_type"] == "parallel_sentence":

            chunk["source_embedding"] = generate_embedding(
                chunk["source_text"]
            )

            chunk["target_embedding"] = generate_embedding(
                chunk["target_text"]
            )

        else:

            chunk["embedding"] = generate_embedding(
                chunk["text"]
            )

        embedded_chunks.append(chunk)

    return embedded_chunks