class VerificationScorer:
    """
    Calculate translation verification score
    for retrieved evidence.
    """

    VERIFICATION_SCORES = {
        "verified": 1.0,
        "approved": 1.0,
        "reviewed": 0.8,
        "pending": 0.5,
        "unverified": 0.2,
        "rejected": 0.0
    }

    def calculate_score(
        self,
        verification_status: str
    ) -> float:
        """
        Return verification score between 0.0 and 1.0.
        """

        if not verification_status:
            return self.VERIFICATION_SCORES["unverified"]

        status = verification_status.lower().strip()

        return self.VERIFICATION_SCORES.get(
            status,
            self.VERIFICATION_SCORES["unverified"]
        )