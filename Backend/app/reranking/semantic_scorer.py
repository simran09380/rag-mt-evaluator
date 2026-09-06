import numpy as np

from app.embeddings.embeddings import generate_embedding


class SemanticScorer:
    """
    Calculate semantic similarity between
    query/source/hypothesis and retrieved evidence.
    """

    @staticmethod
    def cosine_similarity(
        embedding_a: list[float],
        embedding_b: list[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.
        """

        if not embedding_a or not embedding_b:
            return 0.0

        vector_a = np.array(
            embedding_a,
            dtype="float32"
        )

        vector_b = np.array(
            embedding_b,
            dtype="float32"
        )

        norm_a = np.linalg.norm(vector_a)
        norm_b = np.linalg.norm(vector_b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        similarity = np.dot(
            vector_a,
            vector_b
        ) / (norm_a * norm_b)

        return float(similarity)

    def calculate_source_similarity(
        self,
        source_text: str,
        candidate_text: str
    ) -> float:
        """
        Calculate semantic similarity between
        source sentence and retrieved candidate.
        """

        if not source_text or not candidate_text:
            return 0.0

        source_embedding = generate_embedding(
            source_text
        )

        candidate_embedding = generate_embedding(
            candidate_text
        )

        return self.cosine_similarity(
            source_embedding,
            candidate_embedding
        )

    def calculate_hypothesis_similarity(
        self,
        hypothesis_text: str,
        candidate_text: str
    ) -> float:
        """
        Calculate semantic similarity between
        MT hypothesis and retrieved candidate.
        """

        if not hypothesis_text or not candidate_text:
            return 0.0

        hypothesis_embedding = generate_embedding(
            hypothesis_text
        )

        candidate_embedding = generate_embedding(
            candidate_text
        )

        return self.cosine_similarity(
            hypothesis_embedding,
            candidate_embedding
        )

    def calculate_score(
        self,
        source_text: str,
        hypothesis_text: str,
        candidate_text: str,
        source_weight: float = 0.5,
        hypothesis_weight: float = 0.5
    ) -> dict:
        """
        Calculate combined semantic relevance.

        Final score =
            source_similarity * source_weight
            +
            hypothesis_similarity * hypothesis_weight
        """

        source_similarity = (
            self.calculate_source_similarity(
                source_text,
                candidate_text
            )
        )

        hypothesis_similarity = (
            self.calculate_hypothesis_similarity(
                hypothesis_text,
                candidate_text
            )
        )

        semantic_score = (
            source_weight * source_similarity
            + hypothesis_weight * hypothesis_similarity
        )

        return {
            "source_similarity": source_similarity,
            "hypothesis_similarity": hypothesis_similarity,
            "semantic_score": float(semantic_score)
        }