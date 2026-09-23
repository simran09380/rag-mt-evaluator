from typing import Any, Optional


class ScoreFusion:
    """
    Module 10:
    Fuse Module 6, Module 7, Module 8, and Module 9
    evaluation signals into a final translation score.
    """

    # --------------------------------------------------
    # WEIGHTS
    # --------------------------------------------------

    REFERENCE_BASED_WEIGHTS = {
        "reference_metrics": 0.25,
        "llm_evaluation": 0.25,
        "evidence_agreement": 0.20,
        "semantic_adequacy": 0.15,
        "terminology": 0.10,
        "fluency": 0.05,
    }

    REFERENCE_FREE_WEIGHTS = {
        "llm_evaluation": 0.30,
        "source_hypothesis_similarity": 0.20,
        "evidence_agreement": 0.20,
        "terminology": 0.10,
        "named_entity": 0.10,
        "fluency": 0.10,
    }

    # --------------------------------------------------
    # PUBLIC METHOD
    # --------------------------------------------------

    def calculate_score(
        self,
        metrics: dict[str, Any],
        llm_evaluation: dict[str, Any],
        mqm_evaluation: dict[str, Any],
        evidence: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        """
        Calculate the final Module 10 score.

        If a reference is available, reference-based fusion
        is used. Otherwise, reference-free fusion is used.
        """

        evidence = evidence or []

        evaluation = self._extract_llm_evaluation(
            llm_evaluation
        )

        mqm_penalty = self._get_mqm_penalty(
            mqm_evaluation
        )

        # ----------------------------------------------
        # Determine evaluation type
        # ----------------------------------------------

        has_reference = self._has_reference_metrics(
            metrics
        )

        if has_reference:
            return self._calculate_reference_based(
                metrics=metrics,
                evaluation=evaluation,
                mqm_penalty=mqm_penalty,
                evidence=evidence,
                supported_by_evidence=llm_evaluation.get(
                    "supported_by_evidence",
                    False,
                ),
            )

        return self._calculate_reference_free(
            metrics=metrics,
            evaluation=evaluation,
            mqm_penalty=mqm_penalty,
            evidence=evidence,
            supported_by_evidence=llm_evaluation.get(
                "supported_by_evidence",
                False,
            ),
        )

    # ==================================================
    # REFERENCE-BASED
    # ==================================================

    def _calculate_reference_based(
        self,
        metrics: dict[str, Any],
        evaluation: dict[str, Any],
        mqm_penalty: float,
        evidence: list[dict[str, Any]],
        supported_by_evidence: bool,
    ) -> dict[str, Any]:

        # ----------------------------------------------
        # 1. Reference metrics
        # ----------------------------------------------

        reference_metrics = self._calculate_reference_metrics(
            metrics
        )

        # ----------------------------------------------
        # 2. LLM evaluation
        # ----------------------------------------------

        llm_score = self._calculate_llm_score(
            evaluation
        )

        # ----------------------------------------------
        # 3. Evidence agreement
        # ----------------------------------------------

        evidence_agreement = self._calculate_evidence_agreement(
            llm_evaluation=evaluation,
            evidence=evidence,
            supported_by_evidence=supported_by_evidence,
        )

        # ----------------------------------------------
        # 4. Semantic adequacy
        # ----------------------------------------------

        semantic_adequacy = self._calculate_semantic_adequacy(
            evaluation
        )

        # ----------------------------------------------
        # 5. Terminology
        # ----------------------------------------------

        terminology = self._normalize_dimension(
            evaluation.get("terminology")
        )

        # ----------------------------------------------
        # 6. Fluency
        # ----------------------------------------------

        fluency = self._normalize_dimension(
            evaluation.get("fluency")
        )

        # ----------------------------------------------
        # Weighted score
        # ----------------------------------------------

        weighted_score = (
            0.25 * reference_metrics
            + 0.25 * llm_score
            + 0.20 * evidence_agreement
            + 0.15 * semantic_adequacy
            + 0.10 * terminology
            + 0.05 * fluency
        )

        final_score = self._apply_penalty(
            weighted_score,
            mqm_penalty,
        )

        return {
            "evaluation_type": "reference_based",

            "components": {
                "reference_metrics": reference_metrics,
                "llm_evaluation": llm_score,
                "evidence_agreement": evidence_agreement,
                "semantic_adequacy": semantic_adequacy,
                "terminology": terminology,
                "fluency": fluency,
                "mqm_penalty": mqm_penalty,
            },

            "weights": self.REFERENCE_BASED_WEIGHTS,

            "weighted_score": weighted_score * 100,

            "final_score": final_score,

            "score_range": {
                "min": 0,
                "max": 100,
            },
        }

    # ==================================================
    # REFERENCE-FREE
    # ==================================================

    def _calculate_reference_free(
        self,
        metrics: dict[str, Any],
        evaluation: dict[str, Any],
        mqm_penalty: float,
        evidence: list[dict[str, Any]],
        supported_by_evidence: bool,
    ) -> dict[str, Any]:

        # ----------------------------------------------
        # 1. LLM evaluation
        # ----------------------------------------------

        llm_score = self._calculate_llm_score(
            evaluation
        )

        # ----------------------------------------------
        # 2. Source-hypothesis similarity
        # ----------------------------------------------

        source_hypothesis_similarity = (
            self._get_hypothesis_similarity(
                evidence
            )
        )

        # ----------------------------------------------
        # 3. Evidence agreement
        # ----------------------------------------------

        evidence_agreement = self._calculate_evidence_agreement(
            llm_evaluation=evaluation,
            evidence=evidence,
            supported_by_evidence=supported_by_evidence,
        )

        # ----------------------------------------------
        # 4. Terminology
        # ----------------------------------------------

        terminology = self._normalize_dimension(
            evaluation.get("terminology")
        )

        # ----------------------------------------------
        # 5. Named entity
        # ----------------------------------------------

        named_entity = self._normalize_dimension(
            evaluation.get("named_entities")
        )

        # ----------------------------------------------
        # 6. Fluency
        # ----------------------------------------------

        fluency = self._normalize_dimension(
            evaluation.get("fluency")
        )

        # ----------------------------------------------
        # Weighted score
        # ----------------------------------------------

        weighted_score = (
            0.30 * llm_score
            + 0.20 * source_hypothesis_similarity
            + 0.20 * evidence_agreement
            + 0.10 * terminology
            + 0.10 * named_entity
            + 0.10 * fluency
        )

        final_score = self._apply_penalty(
            weighted_score,
            mqm_penalty,
        )

        return {
            "evaluation_type": "reference_free",

            "components": {
                "llm_evaluation": llm_score,
                "source_hypothesis_similarity": (
                    source_hypothesis_similarity
                ),
                "evidence_agreement": evidence_agreement,
                "terminology": terminology,
                "named_entity": named_entity,
                "fluency": fluency,
                "mqm_penalty": mqm_penalty,
            },

            "weights": self.REFERENCE_FREE_WEIGHTS,

            "weighted_score": weighted_score * 100,

            "final_score": final_score,

            "score_range": {
                "min": 0,
                "max": 100,
            },
        }

    # ==================================================
    # MODULE 7
    # ==================================================

    @staticmethod
    def _calculate_reference_metrics(
        metrics: dict[str, Any],
    ) -> float:

        reference_based = metrics.get(
            "reference_based",
            {}
        )

        values = []

        # Higher is better
        higher_is_better = [
            "bleu",
            "chrf",
            "chrf_plus_plus",
            "meteor",
            "bertscore",
            "comet",
        ]

        for metric_name in higher_is_better:

            value = reference_based.get(
                metric_name
            )

            if value is not None:
                values.append(
                    ScoreFusion._clamp(
                        float(value)
                    )
                )

        # TER: lower is better
        ter = reference_based.get("ter")

        if ter is not None:

            ter_score = 1.0 - ScoreFusion._clamp(
                float(ter)
            )

            values.append(ter_score)

        if not values:
            return 0.0

        return sum(values) / len(values)

    # ==================================================
    # MODULE 8
    # ==================================================

    @staticmethod
    def _extract_llm_evaluation(
        llm_evaluation: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Supports:

        {
            "evaluation": {...}
        }

        as well as direct evaluation dictionaries.
        """

        evaluation = llm_evaluation.get(
            "evaluation"
        )

        if isinstance(evaluation, dict):
            return evaluation

        return llm_evaluation

    @staticmethod
    def _calculate_llm_score(
        evaluation: dict[str, Any],
    ) -> float:

        dimensions = [
            "accuracy",
            "fluency",
            "terminology",
            "named_entities",
            "factual_consistency",
            "style",
            "omissions",
            "additions",
        ]

        scores = []

        for dimension in dimensions:

            value = ScoreFusion._extract_dimension_score(
                evaluation.get(dimension)
            )

            if value is not None:

                scores.append(
                    ScoreFusion._clamp(
                        value / 5.0
                    )
                )

        if not scores:
            return 0.0

        return sum(scores) / len(scores)

    @staticmethod
    def _calculate_semantic_adequacy(
        evaluation: dict[str, Any],
    ) -> float:

        accuracy = ScoreFusion._extract_dimension_score(
            evaluation.get("accuracy")
        )

        factual_consistency = (
            ScoreFusion._extract_dimension_score(
                evaluation.get(
                    "factual_consistency"
                )
            )
        )

        values = []

        if accuracy is not None:

            values.append(
                ScoreFusion._clamp(
                    accuracy / 5.0
                )
            )

        if factual_consistency is not None:

            values.append(
                ScoreFusion._clamp(
                    factual_consistency / 5.0
                )
            )

        if not values:
            return 0.0

        return sum(values) / len(values)

    # ==================================================
    # MODULE 6
    # ==================================================

    @staticmethod
    def _get_hypothesis_similarity(
        evidence: list[dict[str, Any]],
    ) -> float:

        scores = []

        for item in evidence:

            if not isinstance(item, dict):
                continue

            value = item.get(
                "hypothesis_similarity"
            )

            if value is not None:

                scores.append(
                    ScoreFusion._clamp(
                        float(value)
                    )
                )

        if not scores:
            return 0.0

        return max(scores)

    @staticmethod
    def _calculate_evidence_agreement(
        llm_evaluation: dict[str, Any],
        evidence: list[dict[str, Any]],
        supported_by_evidence: bool,
    ) -> float:

        if not supported_by_evidence:
            return 0.0

        # ----------------------------------------------
        # Collect evidence IDs cited by the LLM
        # ----------------------------------------------

        evidence_ids = set()

        dimensions = [
            "accuracy",
            "fluency",
            "terminology",
            "named_entities",
            "factual_consistency",
            "style",
            "omissions",
            "additions",
        ]

        for dimension in dimensions:

            result = llm_evaluation.get(
                dimension
            )

            if not isinstance(result, dict):
                continue

            for evidence_id in result.get(
                "evidence_ids",
                []
            ):

                evidence_ids.add(
                    evidence_id
                )

        if not evidence_ids:
            return 0.0

        # ----------------------------------------------
        # Match E1/E2/... with evidence objects
        # ----------------------------------------------

        relevance_scores = []

        for item in evidence:

            if not isinstance(item, dict):
                continue

            if item.get("id") not in evidence_ids:
                continue

            relevance = item.get(
                "relevance"
            )

            if relevance is not None:

                relevance_scores.append(
                    ScoreFusion._clamp(
                        float(relevance)
                    )
                )

        if not relevance_scores:
            return 0.0

        return (
            sum(relevance_scores)
            / len(relevance_scores)
        )

    # ==================================================
    # MODULE 9
    # ==================================================

    @staticmethod
    def _get_mqm_penalty(
        mqm_evaluation: dict[str, Any],
    ) -> float:

        penalty = mqm_evaluation.get(
            "total_penalty",
            0
        )

        try:

            return max(
                0.0,
                float(penalty)
            )

        except (TypeError, ValueError):

            return 0.0

    # ==================================================
    # HELPERS
    # ==================================================

    @staticmethod
    def _normalize_dimension(
        value: Any,
    ) -> float:

        score = ScoreFusion._extract_dimension_score(
            value
        )

        if score is None:
            return 0.0

        return ScoreFusion._clamp(
            score / 5.0
        )

    @staticmethod
    def _extract_dimension_score(
        value: Any,
    ) -> Optional[float]:

        if isinstance(value, dict):

            value = value.get(
                "score"
            )

        if value is None:
            return None

        try:

            return float(value)

        except (TypeError, ValueError):

            return None

    @staticmethod
    def _has_reference_metrics(
        metrics: dict[str, Any],
    ) -> bool:

        reference_based = metrics.get(
            "reference_based"
        )

        if not isinstance(
            reference_based,
            dict
        ):
            return False

        return len(reference_based) > 0

    @staticmethod
    def _apply_penalty(
        weighted_score: float,
        mqm_penalty: float,
    ) -> float:

        score = (
            weighted_score * 100
            - mqm_penalty
        )

        return round(
            max(
                0.0,
                min(
                    100.0,
                    score
                )
            ),
            4
        )

    @staticmethod
    def _clamp(
        value: float,
        minimum: float = 0.0,
        maximum: float = 1.0,
    ) -> float:

        return max(
            minimum,
            min(
                maximum,
                value
            )
        )