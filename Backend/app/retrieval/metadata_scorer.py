class MetadataScorer:
    """
    Calculate metadata relevance between
    a query and a retrieved chunk.
    """

    def __init__(
        self,
        language_weight: float = 0.5,
        domain_weight: float = 0.3,
        chunk_type_weight: float = 0.2
    ):
        self.language_weight = language_weight
        self.domain_weight = domain_weight
        self.chunk_type_weight = chunk_type_weight

    def calculate_score(
        self,
        query_metadata: dict,
        chunk_metadata: dict
    ) -> float:
        """
        Calculate metadata relevance score.

        Score range:
            0.0 -> no metadata match
            1.0 -> complete metadata match
        """

        if not chunk_metadata:
            return 0.0

        score = 0.0

        # -----------------------------------------
        # Language match
        # -----------------------------------------

        query_language = query_metadata.get(
            "language"
        )

        chunk_language = chunk_metadata.get(
            "language"
        )

        if (
            query_language
            and chunk_language
            and query_language == chunk_language
        ):
            score += self.language_weight

        # -----------------------------------------
        # Domain match
        # -----------------------------------------

        query_domain = query_metadata.get(
            "domain"
        )

        chunk_domain = chunk_metadata.get(
            "domain"
        )

        if (
            query_domain
            and chunk_domain
            and query_domain == chunk_domain
        ):
            score += self.domain_weight

        # -----------------------------------------
        # Chunk type match
        # -----------------------------------------

        query_chunk_type = query_metadata.get(
            "chunk_type"
        )

        chunk_type = chunk_metadata.get(
            "chunk_type"
        )

        if (
            query_chunk_type
            and chunk_type
            and query_chunk_type == chunk_type
        ):
            score += self.chunk_type_weight

        return min(score, 1.0)