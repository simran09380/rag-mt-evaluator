class AuthorityScorer:
    """
    Calculate source authority score.

    Score range:
        0.0 -> lowest authority
        1.0 -> highest authority
    """

    AUTHORITY_SCORES = {
        "high": 1.0,
        "medium": 0.7,
        "low": 0.4,
        "unknown": 0.2
    }

    def calculate_score(
        self,
        source_authority: str
    ) -> float:
        """
        Convert source authority level
        into a normalized score.
        """

        if not source_authority:
            return self.AUTHORITY_SCORES["unknown"]

        authority = source_authority.lower().strip()

        return self.AUTHORITY_SCORES.get(
            authority,
            self.AUTHORITY_SCORES["unknown"]
        )