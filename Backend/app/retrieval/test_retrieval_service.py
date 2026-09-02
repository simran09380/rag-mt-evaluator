from app.retrieval.retrieval_service import RetrievalService
from app.indexing.index_manager import IndexManager


# -----------------------------------------
# Load existing FAISS indexes
# -----------------------------------------

index_manager = IndexManager(
    index_dir="indexes"
)


# -----------------------------------------
# Temporary test chunks
# -----------------------------------------
# IMPORTANT:
# These should eventually come from
# Module 4 valid_chunks.

chunks = [
    {
        "chunk_id": "src_1",
        "chunk_type": "sentence",
        "text": (
            "Dr. Sharma prescribed antibiotics "
            "to treat the patient's bacterial infection."
        ),
        "language": "en",
        "domain": "healthcare",
        "authority": "unknown"
    },
    {
        "chunk_id": "src_2",
        "chunk_type": "sentence",
        "text": (
            "The patient should take the medicine "
            "twice a day after meals."
        ),
        "language": "en",
        "domain": "healthcare",
        "authority": "unknown"
    }
]


# -----------------------------------------
# Create Retrieval Service
# -----------------------------------------

retrieval_service = RetrievalService(
    chunks=chunks,
    index_manager=index_manager
)


# -----------------------------------------
# Query
# -----------------------------------------

query = "antibiotics for bacterial infection"


query_metadata = {
    "language": "en",
    "domain": "healthcare",
    "chunk_type": "sentence"
}


# -----------------------------------------
# Hybrid Retrieval
# -----------------------------------------

results = retrieval_service.retrieve(
    query=query,
    query_metadata=query_metadata,
    index_type="source",
    top_k=1
)


# -----------------------------------------
# Display results
# -----------------------------------------

print("\nQuery:")
print(query)

print("\nHybrid Retrieval Results:")

for result in results:

    print("\n------------------------")

    print("Chunk ID:", result["chunk_id"])
    print("Chunk Type:", result["chunk_type"])
    print("Text:", result["text"])

    print(
        "BM25:",
        result["bm25_score"]
    )

    print(
        "Normalized BM25:",
        result["normalized_bm25_score"]
    )

    print(
        "Dense:",
        result["dense_score"]
    )

    print(
        "Normalized Dense:",
        result["normalized_dense_score"]
    )

    print(
        "Metadata:",
        result["metadata_score"]
    )

    print(
        "Authority:",
        result["authority_score"]
    )

    print(
        "Hybrid:",
        result["hybrid_score"]
    )