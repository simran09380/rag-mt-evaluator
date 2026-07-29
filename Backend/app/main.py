from fastapi import FastAPI
from app.schemas import TranslationRequest
from preprocessing.language_detector import detect_language
#from preprocessing.tokenizer import tokenize
from preprocessing.normalizer import normalize_text

app = FastAPI(
    title="RAG MT Evaluator",
    version="1.0"
)


@app.post("/evaluate")
def evaluate(data: TranslationRequest):

    source_language = detect_language(data.source)
    target_language = detect_language(data.hypothesis)

    # source_tokens = tokenize(data.source)
    # target_tokens = tokenize(data.hypothesis)

    normalized_source = normalize_text(data.source)
    normalized_target = normalize_text(data.hypothesis)

    return {
        "source_language": source_language,
        "target_language": target_language,
        # "source_tokens": source_tokens,
        # "target_tokens": target_tokens
         "normalized_source": normalized_source,
        "normalized_target": normalized_target
    }