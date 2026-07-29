import unicodedata
from pathlib import Path

from indicnlp import common
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory

BASE_DIR = Path(__file__).resolve().parent.parent

RESOURCES_PATH = BASE_DIR / "resources" / "indic_nlp_resources"

common.set_resources_path(str(RESOURCES_PATH))

def unicode_normalize(text: str) -> str:
    return unicodedata.normalize("NFC", text)

factory = IndicNormalizerFactory()
hindi_normalizer=factory.get_normalizer("hi")
def normalize_hindi(text: str) -> str:
    return hindi_normalizer.normalize(text)

def normalize_text(text: str, language: str) -> str:
    text = unicode_normalize(text)
    if language == "hi":
        return normalize_hindi(text)
    return text

    
