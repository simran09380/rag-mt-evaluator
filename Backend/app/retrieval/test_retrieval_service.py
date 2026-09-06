from app.retrieval.query_retrieval_service import (
    QueryRetrievalService
)
from app.indexing.index_manager import IndexManager


# =========================================
# Load existing FAISS indexes
# =========================================

index_manager = IndexManager(
    index_dir="indexes"
)


# =========================================
# Test chunks
# =========================================

chunks = [
    {
        "chunk_id": "src_1",
        "chunk_type": "sentence",
        "source_text": (
            "Dr. Sharma prescribed antibiotics "
            "to treat the patient's bacterial infection."
        ),
        "target_text": (
            "डॉ. शर्मा ने मरीज के बैक्टीरियल संक्रमण "
            "के इलाज के लिए एंटीबायोटिक्स लिखीं।"
        ),
        "text": (
            "Dr. Sharma prescribed antibiotics "
            "to treat the patient's bacterial infection."
        ),
        "source_lang": "en",
        "target_lang": "hi",
        "domain": "healthcare",
        "authority": "unknown",
        "terms": [
            "antibiotics",
            "bacterial infection"
        ],
        "entities": [
            "Dr. Sharma"
        ],
        "verification_status": "verified",
        "source_type": "translation_memory"
    },

    {
        "chunk_id": "src_2",
        "chunk_type": "sentence",
        "source_text": (
            "The patient should take the medicine "
            "twice a day after meals."
        ),
        "target_text": (
            "रोगी को भोजन के बाद दिन में दो बार "
            "औषधि लेनी चाहिए।"
        ),
        "text": (
            "The patient should take the medicine "
            "twice a day after meals."
        ),
        "source_lang": "en",
        "target_lang": "hi",
        "domain": "healthcare",
        "authority": "official",
        "terms": [
            "twice daily",
            "medicine"
        ],
        "entities": [],
        "verification_status": "verified",
        "source_type": "translation_memory"
    }
]


# =========================================
# Create Query Retrieval Service
# =========================================

service = QueryRetrievalService(
    chunks=chunks,
    index_manager=index_manager
)


# =========================================
# Source sentence + MT hypothesis
# =========================================

source_text = (
    "The patient should take the medicine "
    "twice a day after meals."
)

mt_output = (
    "रोगी को भोजन के बाद दिन में दो बार "
    "औषधि लेनी चाहिए।"
)


# =========================================
# Module 3 generated queries
# =========================================

generated_queries = {
    "full_sentence": [
        source_text
    ],

    "keywords": [
        "medicine twice day meals"
    ],

    "terminology": [
        "twice daily"
    ],

    "named_entities": [],

    "semantic_embedding": [
        source_text
    ],

    "cross_lingual": [
        mt_output
    ]
}


# =========================================
# Query metadata
# =========================================

query_metadata = {
    "source_lang": "en",
    "target_lang": "hi",
    "domain": "healthcare"
}


# =========================================
# Module 3 → Module 5 → Module 6
# =========================================

results = service.retrieve_generated_queries(
    generated_queries=generated_queries,

    source_text=source_text,
    mt_output=mt_output,

    source_lang="en",
    target_lang="hi",

    query_terms=[
        "medicine",
        "twice daily"
    ],

    query_entities=[],

    query_metadata=query_metadata,

    index_type="source",

    # Module 6 final output
    top_k=3,

    # Module 5 candidate pool
    retrieval_top_k=5
)


# =========================================
# Display final results
# =========================================

print("\n")
print("=" * 60)
print("MODULE 3 → MODULE 5 → MODULE 6")
print("=" * 60)

print("\nSource:")
print(source_text)

print("\nMT Output:")
print(mt_output)


for query_type, query_results in results.items():

    print("\n")
    print("=" * 60)
    print("QUERY TYPE:", query_type)
    print("=" * 60)

    if isinstance(query_results, list):

        for item in query_results:

            print("\nQuery:")
            print(item["query"])

            print("\nReranked Evidence:")

            for rank, result in enumerate(
                item["results"],
                start=1
            ):

                print("\n------------------------")
                print("Rank:", rank)
                print("Chunk ID:", result["chunk_id"])
                print(
                    "Source:",
                    result["source"]
                )
                print(
                    "Target:",
                    result["target"]
                )
                print(
                    "Source Type:",
                    result["source_type"]
                )
                print(
                    "Source Similarity:",
                    round(
                        result["source_similarity"],
                        4
                    )
                )
                print(
                    "Hypothesis Similarity:",
                    round(
                        result["hypothesis_similarity"],
                        4
                    )
                )
                print(
                    "Language Pair:",
                    round(
                        result["language_pair_score"],
                        4
                    )
                )
                print(
                    "Terminology:",
                    round(
                        result["terminology_score"],
                        4
                    )
                )
                print(
                    "Entity:",
                    round(
                        result["entity_score"],
                        4
                    )
                )
                print(
                    "Authority:",
                    round(
                        result["authority_score"],
                        4
                    )
                )
                print(
                    "Verification:",
                    round(
                        result["verification_score"],
                        4
                    )
                )
                print(
                    "FINAL RELEVANCE:",
                    round(
                        result["relevance"],
                        4
                    )
                )

    else:

        print("\nQuery:")
        print(query_results["query"])

        print("\nReranked Evidence:")

        for rank, result in enumerate(
            query_results["results"],
            start=1
        ):

            print("\n------------------------")
            print("Rank:", rank)
            print("Chunk ID:", result["chunk_id"])
            print("Source:", result["source"])
            print("Target:", result["target"])
            print(
                "FINAL RELEVANCE:",
                round(
                    result["relevance"],
                    4
                )
            )