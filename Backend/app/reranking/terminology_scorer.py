class TerminologyScorer:
    """
    Calculate terminology overlap between
    the query and retrieved evidence.
    """

    def calculate_score(
        self,
        query_terms: list[str],
        candidate_terms: list[str]
    ) -> float:
        """
        Calculate terminology overlap.

        Score = matched terms / query terms
        """

        if not query_terms or not candidate_terms:
            return 0.0

        # Normalize terms
        query_set = {
            term.lower().strip()
            for term in query_terms
            if term and term.strip()
        }

        candidate_set = {
            term.lower().strip()
            for term in candidate_terms
            if term and term.strip()
        }

        if not query_set:
            return 0.0

        matched_terms = query_set.intersection(
            candidate_set
        )

        score = len(matched_terms) / len(query_set)

        return float(score)