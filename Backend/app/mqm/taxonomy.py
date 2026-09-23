from enum import Enum


class MQMCategory(str, Enum):
    ACCURACY = "accuracy"
    FLUENCY = "fluency"
    TERMINOLOGY = "terminology"
    NAMED_ENTITY = "named_entity"
    STYLE = "style"


class MQMSeverity(str, Enum):
    NEUTRAL = "neutral"
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"


MQM_TAXONOMY = {
    "accuracy": [
        "mistranslation",
        "omission",
        "addition",
        "untranslated_text",
        "overtranslation",
        "undertranslation",
        "incorrect_relation",
        "factual_inconsistency",
    ],

    "fluency": [
        "grammar",
        "spelling",
        "punctuation",
        "word_order",
        "agreement",
        "awkward_expression",
        "sentence_structure",
    ],

    "terminology": [
        "incorrect_term",
        "inconsistent_terminology",
        "domain_inappropriate_term",
        "untranslated_technical_term",
    ],

    "named_entity": [
        "incorrect_translation",
        "incorrect_transliteration",
        "omitted_entity",
        "changed_entity",
        "wrong_entity_type",
    ],

    "style": [
        "inappropriate_register",
        "excessive_literalness",
        "cultural_inappropriateness",
        "politeness_mismatch",
        "inconsistent_style",
    ],
}


SEVERITY_PENALTIES = {
    "neutral": 0,
    "minor": 1,
    "major": 5,
    "critical": 10,
}