import sacrebleu
from nltk.translate.meteor_score import meteor_score
from bert_score import score as bert_score
from comet import download_model, load_from_checkpoint

COMET_MODEL = "Unbabel/wmt22-comet-da"

_comet_model = None


def get_comet_model():
    global _comet_model

    if _comet_model is None:
        model_path = download_model(COMET_MODEL)
        _comet_model = load_from_checkpoint(model_path)

    return _comet_model

def calculate_meteor(hypothesis: str, reference: str) -> float:
    """
    Calculate METEOR score between hypothesis and reference.
    """

    hypothesis_tokens = hypothesis.split()
    reference_tokens = reference.split()

    score = meteor_score(
        [reference_tokens],
        hypothesis_tokens
    )

    return score

def calculate_bleu(hypothesis: str, reference: str) -> float:
    """
    Calculate BLEU score between hypothesis and reference translation.
    """
    score = sacrebleu.corpus_bleu(
        [hypothesis],
        [[reference]]
    )

    return score.score / 100


def calculate_chrf(hypothesis: str, reference: str) -> float:
    """
    Calculate chrF score between hypothesis and reference translation.
    """
    score = sacrebleu.corpus_chrf(
        [hypothesis],
        [[reference]]
    )

    return score.score / 100


def calculate_chrf_plus_plus(hypothesis: str, reference: str) -> float:
    """
    Calculate chrF++ score using word_order=2.
    """
    score = sacrebleu.corpus_chrf(
        [hypothesis],
        [[reference]],
        word_order=2
    )

    return score.score / 100


def calculate_ter(hypothesis: str, reference: str) -> float:
    """
    Calculate Translation Edit Rate (TER).
    Lower TER is better.
    """
    score = sacrebleu.corpus_ter(
        [hypothesis],
        [[reference]]
    )

    return score.score / 100

def calculate_bertscore(
    hypothesis: str,
    reference: str,
    language: str = "en"
) -> float:
    """
    Calculate multilingual BERTScore F1 between hypothesis and reference.
    """

    _, _, f1 = bert_score(
        [hypothesis],
        [reference],
        lang=language
    )

    return float(f1[0])

def calculate_comet(
    source: str,
    hypothesis: str,
    reference: str
) -> float:
    """
    Calculate COMET score using source, hypothesis and reference.
    """

    model = get_comet_model()

    data = [
        {
            "src": source,
            "mt": hypothesis,
            "ref": reference
        }
    ]

    prediction = model.predict(
        data,
        batch_size=1,
        gpus=0
    )

    return float(prediction.system_score)

