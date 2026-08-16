from typing import List


class EmbeddingGenerator:
    """
    Generate vector embeddings for text chunks.

    The actual embedding model can be configured later.
    """

    def __init__(self, model):
        self.model = model

    def generate(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        """

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()