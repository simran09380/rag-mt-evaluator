from app.retrieval.authority_scorer import AuthorityScorer


class RerankingAuthorityScorer:
    """
    Calculate document authority score
    for retrieval reranking.
    """

    def __init__(self):
        self.authority_scorer = AuthorityScorer()

    def calculate_score(
        self,
        source_authority: str
    ) -> float:
        """
        Return authority score between 0.0 and 1.0.
        """

        return self.authority_scorer.calculate_score(
            source_authority
        )