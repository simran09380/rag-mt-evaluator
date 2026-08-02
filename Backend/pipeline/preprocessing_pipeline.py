from preprocessing.language_detector import detect_language
from preprocessing.normalizer import normalize_text
from preprocessing.sentence_segmenter import segment_text
from preprocessing.tokenizer import tokenize_text
from preprocessing.pos_tagger import tag_text
from preprocessing.ner import extract_entities
from preprocessing.terminology_extractor import extract_terminology
from preprocessing.dependency_parser import parse_text

def preprocess(source: str, hypothesis: str):
    source_language = detect_language(source)
    target_language = detect_language(hypothesis)

    normalized_source = normalize_text(
    source,
    source_language
    )

    normalized_target = normalize_text(
        hypothesis,
        target_language
    )

    source_sentences = segment_text(
        normalized_source,
        source_language
    )

    target_sentences = segment_text(
        normalized_target,
        target_language
    )
    source_tokens = tokenize_text(
    source_sentences,
    source_language
    )

    target_tokens = tokenize_text(
        target_sentences,
        target_language
    )
    source_pos = tag_text(
    source_sentences,
    source_language
    )

    target_pos = tag_text(
        target_sentences,
        target_language
    )
    source_entities = []

    for sentence in source_sentences:

        source_entities.append(
            extract_entities(
                sentence,
                source_language
            )
        )

    target_entities = []

    for sentence in target_sentences:

        target_entities.append(
            extract_entities(
                sentence,
                target_language
            )
        )
    source_terminology = extract_terminology(
    normalized_source,
    source_language
    )

    target_terminology = extract_terminology(
        normalized_target,
        target_language
       
    )
    source_dependency = parse_text(
    source_sentences,
    source_language
    )

    target_dependency = parse_text(
        target_sentences,
        target_language
    )
    return {
    "source_language": source_language,
    "target_language": target_language,
    "normalized_source": normalized_source,
    "normalized_target": normalized_target,
    "source_sentences": source_sentences,
    "target_sentences": target_sentences,
    "source_tokens": source_tokens,
    "target_tokens": target_tokens,
    "source_pos": source_pos,
    "target_pos": target_pos,
    "source_entities": source_entities,
    "target_entities": target_entities,
    "source_terminology": source_terminology,
    "target_terminology": target_terminology,
    "source_dependency": source_dependency,
    "target_dependency": target_dependency,
    }