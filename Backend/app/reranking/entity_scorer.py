class EntityScorer:
    """
    Calculate named entity overlap between
    the query and retrieved evidence.
    """

    def calculate_score(
        self,
        query_entities: list[str],
        candidate_entities: list[str]
    ) -> float:
        """
        Calculate entity overlap.

        Score = matched entities / query entities
        """

        if not query_entities or not candidate_entities:
            return 0.0

        # Normalize entities
        query_set = {
            entity.lower().strip()
            for entity in query_entities
            if entity and entity.strip()
        }

        candidate_set = {
            entity.lower().strip()
            for entity in candidate_entities
            if entity and entity.strip()
        }

        if not query_set:
            return 0.0

        matched_entities = query_set.intersection(
            candidate_set
        )

        score = len(matched_entities) / len(query_set)

        return float(score)