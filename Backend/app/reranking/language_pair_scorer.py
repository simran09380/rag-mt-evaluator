class LanguagePairScorer:
    """
    Calculate language-pair compatibility
    between the query and retrieved evidence.
    """

    def calculate_score(
        self,
        query_source_lang: str,
        query_target_lang: str,
        candidate_source_lang: str,
        candidate_target_lang: str
    ) -> float:
        """
        Return a compatibility score between 0.0 and 1.0.
        """

        if not query_source_lang or not query_target_lang:
            return 0.0

        if not candidate_source_lang or not candidate_target_lang:
            return 0.0

        query_source_lang = query_source_lang.lower().strip()
        query_target_lang = query_target_lang.lower().strip()

        candidate_source_lang = (
            candidate_source_lang.lower().strip()
        )
        candidate_target_lang = (
            candidate_target_lang.lower().strip()
        )

        # Exact language-pair match
        if (
            query_source_lang == candidate_source_lang
            and
            query_target_lang == candidate_target_lang
        ):
            return 1.0

        # Source language matches
        if query_source_lang == candidate_source_lang:
            return 0.5

        # Target language matches
        if query_target_lang == candidate_target_lang:
            return 0.5

        # No compatibility
        return 0.0