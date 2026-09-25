from app.metrics.reference_metrics import (
    calculate_bleu,
    calculate_chrf,
    calculate_chrf_plus_plus,
    calculate_meteor,
    calculate_ter,
    calculate_bertscore,
    calculate_comet,
)

from app.metrics.reference_free_metrics import (
    calculate_multilingual_similarity,
    calculate_word_alignment_coverage,
    calculate_entity_preservation,
    calculate_terminology_accuracy,
    calculate_length_ratio,
    calculate_untranslated_token_ratio,
)


def calculate_all_metrics(
    source: str,
    hypothesis: str,
    reference: str
) -> dict:
    """
    Calculate all Module 7 translation evaluation metrics.
    """

    # Reference-based metrics
    reference_based = {}
    if reference and reference.strip():
        reference_based ={
            "bleu": calculate_bleu(
                hypothesis,
                reference
            ),

            "chrf": calculate_chrf(
                hypothesis,
                reference
            ),

            "chrf_plus_plus": calculate_chrf_plus_plus(
                hypothesis,
                reference
            ),

            "meteor": calculate_meteor(
                hypothesis,
                reference
            ),

            "ter": calculate_ter(
                hypothesis,
                reference
            ),

            "bertscore": calculate_bertscore(
                hypothesis,
                reference
            ),

            "comet": calculate_comet(
                source,
                hypothesis,
                reference
            ),
    }

    # Reference-free metrics
    reference_free = {
        "multilingual_similarity": calculate_multilingual_similarity(
            source,
            hypothesis
        ),

        "word_alignment_coverage": calculate_word_alignment_coverage(
            source,
            hypothesis
        ),

        "entity_preservation": calculate_entity_preservation(
            source,
            hypothesis
        ),

        "terminology_accuracy": calculate_terminology_accuracy(
            source,
            hypothesis
        ),

        "length_ratio": calculate_length_ratio(
            source,
            hypothesis
        ),

        "untranslated_token_ratio": calculate_untranslated_token_ratio(
            source,
            hypothesis
        ),
    }

    return {
        "reference_based": reference_based,
        "reference_free": reference_free
    }


