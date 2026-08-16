from app.query_generation.full_sentence import (
    generate_full_sentence_query
)
from app.query_generation.keyword_query import (
    generate_keyword_query
)
from app.query_generation.terminology_query import (
    generate_terminology_query
)
from app.query_generation.ner_query import (
    generate_ner_query
)
from app.query_generation.semantic_query import (
    generate_semantic_query
)
from app.query_generation.cross_lingual_query import (
    generate_cross_lingual_query
)


def generate_queries(
    source_text: str,
    mt_output: str,
    source_lang: str,
    target_lang: str,
    domain: str
) -> dict:
    """
    Generate all retrieval query types
    for a source sentence and its MT output.
    """

    return {
        "full_sentence": generate_full_sentence_query(
            source_text
        ),

        "keywords": generate_keyword_query(
            source_text
        ),

        "terminology": generate_terminology_query(
            text=source_text,
            domain=domain,
            source_lang=source_lang,
            target_lang=target_lang
        ),

        "named_entities": generate_ner_query(
            text=source_text,
            target_lang=target_lang
        ),

        "semantic_embedding": generate_semantic_query(
            source_text
        ),

        "cross_lingual": generate_cross_lingual_query(
            source_text=source_text,
            mt_output=mt_output
        )
    }