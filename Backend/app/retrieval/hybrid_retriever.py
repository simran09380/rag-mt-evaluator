from app.retrieval.score_normalizer import ScoreNormalizer


class HybridRetriever:
    """
    Hybrid retrieval combining:

    1. BM25 lexical retrieval
    2. Dense semantic retrieval
    3. Metadata relevance
    4. Source authority
    """

    def __init__(
        self,
        bm25_retriever,
        dense_retriever,
        metadata_scorer,
        authority_scorer,
        alpha: float = 0.25,
        beta: float = 0.45,
        gamma: float = 0.15,
        delta: float = 0.15
    ):

        self.bm25_retriever = bm25_retriever
        self.dense_retriever = dense_retriever
        self.metadata_scorer = metadata_scorer
        self.authority_scorer = authority_scorer

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta

    def retrieve(
        self,
        query: str,
        query_metadata: dict | None = None,
        index_type: str = "source",
        top_k: int = 5
    ) -> list[dict]:
        """
        Perform complete hybrid retrieval.
        """

        if not query or not query.strip():
            return []

        query_metadata = query_metadata or {}

        # ==========================================
        # 1. BM25 RETRIEVAL
        # ==========================================

        bm25_results = self.bm25_retriever.retrieve(
            query=query,
            top_k=top_k
        )

        # ==========================================
        # 2. DENSE RETRIEVAL
        # ==========================================

        dense_results = self.dense_retriever.retrieve(
            query=query,
            index_type=index_type,
            top_k=top_k
        )

        # ==========================================
        # 3. MERGE CANDIDATES
        # ==========================================

        candidates = {}

        for result in bm25_results:

            chunk_id = result.get("chunk_id")

            if chunk_id is None:
                continue

            candidates[chunk_id] = {
                "chunk_id": chunk_id,
                "chunk_type": result.get(
                    "chunk_type"
                ),
                "text": result.get("text", ""),
                "metadata": result.get(
                    "metadata", {}
                ),
                "bm25_score": result.get(
                    "bm25_score", 0.0
                ),
                "dense_score": 0.0
            }

        for result in dense_results:

            chunk_id = result.get("chunk_id")

            if chunk_id is None:
                continue

            if chunk_id not in candidates:

                candidates[chunk_id] = {
                    "chunk_id": chunk_id,
                    "chunk_type": result.get(
                        "chunk_type"
                    ),
                    "text": result.get("text", ""),
                    "metadata": result.get(
                        "metadata", {}
                    ),
                    "bm25_score": 0.0,
                    "dense_score": result.get(
                        "dense_score", 0.0
                    )
                }

            else:

                candidates[chunk_id][
                    "dense_score"
                ] = result.get(
                    "dense_score", 0.0
                )

        # ==========================================
        # 4. NORMALIZE BM25 SCORES
        # ==========================================

        candidate_list = list(
            candidates.values()
        )

        bm25_scores = [
            candidate["bm25_score"]
            for candidate in candidate_list
        ]

        normalized_bm25 = (
            ScoreNormalizer.min_max_normalize(
                bm25_scores
            )
        )

        # ==========================================
        # 5. NORMALIZE DENSE SCORES
        # ==========================================

        dense_scores = [
            candidate["dense_score"]
            for candidate in candidate_list
        ]

        normalized_dense = (
            ScoreNormalizer.min_max_normalize(
                dense_scores
            )
        )

        # ==========================================
        # 6. CALCULATE METADATA + AUTHORITY
        # ==========================================

        for i, candidate in enumerate(
            candidate_list
        ):

            chunk_metadata = candidate.get(
                "metadata", {}
            )

            metadata_score = (
                self.metadata_scorer.calculate_score(
                    query_metadata=query_metadata,
                    chunk_metadata=chunk_metadata
                )
            )

            authority = chunk_metadata.get(
                "authority",
                "unknown"
            )

            authority_score = (
                self.authority_scorer.calculate_score(
                    authority
                )
            )

            candidate[
                "normalized_bm25_score"
            ] = normalized_bm25[i]

            candidate[
                "normalized_dense_score"
            ] = normalized_dense[i]

            candidate[
                "metadata_score"
            ] = metadata_score

            candidate[
                "authority_score"
            ] = authority_score

            # ======================================
            # 7. FINAL HYBRID SCORE
            # ======================================

            candidate[
                "hybrid_score"
            ] = (
                self.alpha
                * normalized_bm25[i]
                +
                self.beta
                * normalized_dense[i]
                +
                self.gamma
                * metadata_score
                +
                self.delta
                * authority_score
            )

        # ==========================================
        # 8. SORT BY HYBRID SCORE
        # ==========================================

        candidate_list.sort(
            key=lambda x: x["hybrid_score"],
            reverse=True
        )

        return candidate_list[:top_k]