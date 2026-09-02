import faiss
import numpy as np

from app.embeddings.embeddings import generate_embedding



class DenseRetriever:
    """
    Semantic retrieval using FAISS
    and multilingual dense embeddings.
    """

    def __init__(
        self,
        index_manager
    ):
        """
        Initialize DenseRetriever
        using the existing IndexManager.
        """

        self.index_manager = index_manager

    def retrieve(
        self,
        query: str,
        index_type: str = "source",
        top_k: int = 5
    ) -> list[dict]:
        """
        Retrieve semantically similar chunks
        from the selected FAISS index.
        """

        if not query or not query.strip():
            return []

        # ---------------------------------------------
        # 1. Get FAISS index
        # ---------------------------------------------

        index = self.index_manager.indexes.get(
            index_type
        )

        if index is None:
            return []

        # ---------------------------------------------
        # 2. Generate query embedding
        # ---------------------------------------------

        query_embedding = generate_embedding(
            query
        )

        if not query_embedding:
            return []

        # ---------------------------------------------
        # 3. Convert to numpy
        # ---------------------------------------------

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        # ---------------------------------------------
        # 4. Normalize
        # ---------------------------------------------

        faiss.normalize_L2(
            query_vector
        )

        # ---------------------------------------------
        # 5. Search FAISS
        # ---------------------------------------------

        scores, indices = index.search(
            query_vector,
            top_k
        )

        # ---------------------------------------------
        # 6. Get corresponding metadata
        # ---------------------------------------------

        metadata = self.index_manager.metadata.get(
            index_type,
            []
        )

        results = []

        for score, index_id in zip(
            scores[0],
            indices[0]
        ):

            # FAISS uses -1 when no result exists
            if index_id == -1:
                continue

            if index_id >= len(metadata):
                continue

            chunk = metadata[index_id]

            results.append({
                "chunk_id": chunk.get(
                    "chunk_id"
                ),
                "chunk_type": chunk.get(
                    "chunk_type"
                ),
                "text": self._get_text(
                    chunk
                ),
                "dense_score": float(
                    score
                ),
                "metadata": chunk
            })

        return results

    @staticmethod
    def _get_text(
        chunk: dict
    ) -> str:
        """
        Extract searchable text from
        different chunk types.
        """

        if chunk.get("text"):
            return chunk["text"]

        if chunk.get("source_text"):
            return chunk["source_text"]

        if chunk.get("target_text"):
            return chunk["target_text"]

        return ""