from app.reranking.reranker import Reranker


def main():

    # -----------------------------------------
    # Original translation input
    # -----------------------------------------

    source_text = (
        "The patient should take the medicine "
        "twice a day after meals."
    )

    hypothesis_text = (
        "मरीज को भोजन के बाद दिन में दो बार "
        "दवा लेनी चाहिए।"
    )

    # -----------------------------------------
    # Simulated candidates from Module 5
    # -----------------------------------------

    candidates = [
        {
            "chunk_id": "src_3",
            "chunk_type": "sentence",
            "text": (
                "The patient should take the medicine "
                "twice a day after meals."
            ),
            "metadata": {
                "source": (
                    "The patient should take the medicine "
                    "twice a day after meals."
                ),
                "target": (
                    "रोगी को भोजन के बाद दिन में दो बार "
                    "औषधि लेनी चाहिए।"
                ),
                "source_lang": "en",
                "target_lang": "hi",
                "domain": "healthcare",
                "authority": "high",
                "verification_status": "verified",
                "terms": [
                    "medicine",
                    "twice a day",
                    "meals"
                ],
                "entities": []
            }
        },

        {
            "chunk_id": "term_1",
            "chunk_type": "term",
            "text": "twice daily",
            "metadata": {
                "term": "twice daily",
                "target_term": "दिन में दो बार",
                "source_lang": "en",
                "target_lang": "hi",
                "domain": "healthcare",
                "authority": "medium",
                "verification_status": "approved",
                "terms": [
                    "twice daily"
                ],
                "entities": []
            }
        },

        {
            "chunk_id": "src_1",
            "chunk_type": "sentence",
            "text": (
                "Dr. Sharma prescribed antibiotics "
                "to treat the patient's bacterial infection."
            ),
            "metadata": {
                "source": (
                    "Dr. Sharma prescribed antibiotics "
                    "to treat the patient's bacterial infection."
                ),
                "target": (
                    "डॉ. शर्मा ने मरीज के बैक्टीरियल "
                    "संक्रमण के इलाज के लिए एंटीबायोटिक्स लिखीं।"
                ),
                "source_lang": "en",
                "target_lang": "hi",
                "domain": "healthcare",
                "authority": "unknown",
                "verification_status": "unverified",
                "terms": [
                    "antibiotics",
                    "bacterial infection"
                ],
                "entities": [
                    "Dr. Sharma"
                ]
            }
        }
    ]

    # -----------------------------------------
    # Query terminology
    # -----------------------------------------

    query_terms = [
        "medicine",
        "twice a day",
        "meals"
    ]

    # -----------------------------------------
    # Query entities
    # -----------------------------------------

    query_entities = []

    # -----------------------------------------
    # Create reranker
    # -----------------------------------------

    reranker = Reranker()

    # -----------------------------------------
    # Run reranking
    # -----------------------------------------

    results = reranker.rerank(
        source_text=source_text,
        hypothesis_text=hypothesis_text,
        candidates=candidates,
        source_lang="en",
        target_lang="hi",
        query_terms=query_terms,
        query_entities=query_entities,
        top_k=3
    )

    # -----------------------------------------
    # Print results
    # -----------------------------------------

    print("\n========== RERANKING RESULTS ==========\n")

    for rank, result in enumerate(results, start=1):

        print(f"Rank: {rank}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Chunk Type: {result['chunk_type']}")
        print(f"Source: {result['source']}")
        print(f"Target: {result['target']}")
        print(f"Source Similarity: {result['source_similarity']:.4f}")
        print(
            f"Hypothesis Similarity: "
            f"{result['hypothesis_similarity']:.4f}"
        )
        print(
            f"Language Pair Score: "
            f"{result['language_pair_score']:.4f}"
        )
        print(
            f"Terminology Score: "
            f"{result['terminology_score']:.4f}"
        )
        print(
            f"Entity Score: "
            f"{result['entity_score']:.4f}"
        )
        print(
            f"Authority Score: "
            f"{result['authority_score']:.4f}"
        )
        print(
            f"Verification Score: "
            f"{result['verification_score']:.4f}"
        )
        print(
            f"Final Relevance: "
            f"{result['relevance']:.4f}"
        )
        print("-" * 50)


if __name__ == "__main__":
    main()