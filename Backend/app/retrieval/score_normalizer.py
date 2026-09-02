class ScoreNormalizer:
    """
    Normalize retrieval scores to a 0-1 range.
    """

    @staticmethod
    def min_max_normalize(scores: list[float]) -> list[float]:
        if not scores:
            return []

        min_score = min(scores)
        max_score = max(scores)

        # If all scores are zero,
        # no candidate received a meaningful score.
        if max_score == min_score:
            if max_score == 0:
                return [0.0 for _ in scores]

            return [1.0 for _ in scores]

        return [
            (score - min_score) / (max_score - min_score)
            for score in scores
        ]