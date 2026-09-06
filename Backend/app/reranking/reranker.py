from app.reranking.semantic_scorer import SemanticScorer
from app.reranking.language_pair_scorer import LanguagePairScorer
from app.reranking.terminology_scorer import TerminologyScorer
from app.reranking.entity_scorer import EntityScorer
from app.reranking.authority_scorer import RerankingAuthorityScorer
from app.reranking.verification_scorer import VerificationScorer


class Reranker:
    """
    Rerank retrieved candidates using multiple
    relevance features.
    """

    def __init__(
        self,
        semantic_weight: float = 0.30,
        language_pair_weight: float = 0.10,
        terminology_weight: float = 0.15,
        entity_weight: float = 0.10,
        authority_weight: float = 0.10,
        verification_weight: float = 0.25
    ):
        self.semantic_scorer = SemanticScorer()
        self.language_pair_scorer = LanguagePairScorer()
        self.terminology_scorer = TerminologyScorer()
        self.entity_scorer = EntityScorer()
        self.authority_scorer = RerankingAuthorityScorer()
        self.verification_scorer = VerificationScorer()

        self.semantic_weight = semantic_weight
        self.language_pair_weight = language_pair_weight
        self.terminology_weight = terminology_weight
        self.entity_weight = entity_weight
        self.authority_weight = authority_weight
        self.verification_weight = verification_weight

    def rerank(
        self,
        source_text: str,
        hypothesis_text: str,
        candidates: list[dict],
        source_lang: str | None = None,
        target_lang: str | None = None,
        query_terms: list[str] | None = None,
        query_entities: list[str] | None = None,
        top_k: int = 5
    ) -> list[dict]:
        """
        Rerank retrieved candidates and return
        the top-k most relevant evidence pieces.
        """

        if not candidates:
            return []

        query_terms = query_terms or []
        query_entities = query_entities or []

        reranked_candidates = []

        for candidate in candidates:

            metadata = candidate.get(
                "metadata",
                {}
            )

            candidate_text = self._get_candidate_text(
                candidate
            )

            # --------------------------------
            # 1. Semantic similarity
            # --------------------------------

            semantic_result = (
                self.semantic_scorer.calculate_score(
                    source_text=source_text,
                    hypothesis_text=hypothesis_text,
                    candidate_text=candidate_text
                )
            )

            semantic_score = semantic_result[
                "semantic_score"
            ]

            # --------------------------------
            # 2. Language-pair compatibility
            # --------------------------------

            language_pair_score = (
                self.language_pair_scorer.calculate_score(
                    query_source_lang=source_lang,
                    query_target_lang=target_lang,
                    candidate_source_lang=metadata.get(
                        "source_lang"
                    ),
                    candidate_target_lang=metadata.get(
                        "target_lang"
                    )
                )
            )

            # --------------------------------
            # 3. Terminology overlap
            # --------------------------------

            candidate_terms = self._get_candidate_terms(
                metadata
            )

            terminology_score = (
                self.terminology_scorer.calculate_score(
                    query_terms=query_terms,
                    candidate_terms=candidate_terms
                )
            )

            # --------------------------------
            # 4. Entity overlap
            # --------------------------------

            candidate_entities = (
                self._get_candidate_entities(
                    metadata
                )
            )

            entity_score = (
                self.entity_scorer.calculate_score(
                    query_entities=query_entities,
                    candidate_entities=candidate_entities
                )
            )

            # --------------------------------
            # 5. Document authority
            # --------------------------------

            authority_score = (
                self.authority_scorer.calculate_score(
                    metadata.get(
                        "authority",
                        "unknown"
                    )
                )
            )

            # --------------------------------
            # 6. Translation verification
            # --------------------------------

            verification_score = (
                self.verification_scorer.calculate_score(
                    metadata.get(
                        "verification_status",
                        "unverified"
                    )
                )
            )

            # --------------------------------
            # Final relevance score
            # --------------------------------

            relevance = (
                self.semantic_weight * semantic_score
                + self.language_pair_weight * language_pair_score
                + self.terminology_weight * terminology_score
                + self.entity_weight * entity_score
                + self.authority_weight * authority_score
                + self.verification_weight * verification_score
            )

            result = {
                "source": metadata.get(
                    "source",
                    candidate_text
                ),
                "target": metadata.get(
                    "target",
                    metadata.get(
                        "target_text",
                        ""
                    )
                ),
                "text": candidate_text,
                "chunk_id": candidate.get(
                    "chunk_id"
                ),
                "chunk_type": candidate.get(
                    "chunk_type"
                ),
                "source_type": metadata.get(
                    "source_type",
                    "unknown"
                ),

                "semantic_score": semantic_score,
                "source_similarity": semantic_result[
                    "source_similarity"
                ],
                "hypothesis_similarity": semantic_result[
                    "hypothesis_similarity"
                ],

                "language_pair_score": language_pair_score,
                "terminology_score": terminology_score,
                "entity_score": entity_score,
                "authority_score": authority_score,
                "verification_score": verification_score,

                "relevance": float(relevance),

                "metadata": metadata
            }

            reranked_candidates.append(
                result
            )

        # Highest relevance first
        reranked_candidates.sort(
            key=lambda x: x["relevance"],
            reverse=True
        )

        return reranked_candidates[:top_k]

    @staticmethod
    def _get_candidate_text(
        candidate: dict
    ) -> str:
        """
        Extract text from different chunk types.
        """

        if candidate.get("text"):
            return candidate["text"]

        metadata = candidate.get(
            "metadata",
            {}
        )

        if metadata.get("text"):
            return metadata["text"]

        if metadata.get("source_text"):
            return metadata["source_text"]

        if metadata.get("target_text"):
            return metadata["target_text"]

        if metadata.get("term"):
            return metadata["term"]

        if metadata.get("entity"):
            return metadata["entity"]

        return ""

    @staticmethod
    def _get_candidate_terms(
        metadata: dict
    ) -> list[str]:
        """
        Extract terminology information
        from candidate metadata.
        """

        terms = metadata.get(
            "terms",
            []
        )

        if isinstance(terms, str):
            return [terms]

        if isinstance(terms, list):
            return terms

        if metadata.get("term"):
            return [metadata["term"]]

        return []

    @staticmethod
    def _get_candidate_entities(
        metadata: dict
    ) -> list[str]:
        """
        Extract named entity information
        from candidate metadata.
        """

        entities = metadata.get(
            "entities",
            []
        )

        if isinstance(entities, str):
            return [entities]

        if isinstance(entities, list):
            return entities

        if metadata.get("entity"):
            return [metadata["entity"]]

        return []