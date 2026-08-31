# import faiss
# import numpy as np
# from pathlib import Path
# import json


# # Embedding dimension of
# # paraphrase-multilingual-MiniLM-L12-v2
# EMBEDDING_DIMENSION = 384


# def build_faiss_index(
#     embeddings: list[list[float]]
# ):
#     """
#     Build a FAISS index from embedding vectors.

#     Cosine similarity is used by normalizing
#     the vectors and using Inner Product.
#     """

#     if not embeddings:
#         return None

#     vectors = np.array(
#         embeddings,
#         dtype="float32"
#     )

#     # Normalize vectors for cosine similarity
#     faiss.normalize_L2(vectors)

#     # Inner Product on normalized vectors
#     # = Cosine Similarity
#     index = faiss.IndexFlatIP(
#         EMBEDDING_DIMENSION
#     )

#     index.add(vectors)

#     return index


# def save_index(
#     index,
#     metadata: list[dict],
#     index_path: str,
#     metadata_path: str
# ):
#     """
#     Save FAISS index and corresponding metadata.
#     """

#     if index is None:
#         return

#     # Create directories if required
#     Path(index_path).parent.mkdir(
#         parents=True,
#         exist_ok=True
#     )

#     # Save FAISS index
#     faiss.write_index(
#         index,
#         index_path
#     )

#     # Save metadata
#     with open(
#         metadata_path,
#         "w",
#         encoding="utf-8"
#     ) as file:

#         json.dump(
#             metadata,
#             file,
#             ensure_ascii=False,
#             indent=2
#         )


# def build_source_index(
#     embedded_chunks: list[dict]
# ):
#     """
#     Build index for source-language
#     sentence chunks.
#     """

#     embeddings = []
#     metadata = []

#     for chunk in embedded_chunks:

#         if (
#             chunk.get("chunk_type") == "sentence"
#             and chunk.get("chunk_id", "").startswith("src_")
#         ):

#             embedding = chunk.get("embedding")

#             if embedding:
#                 embeddings.append(embedding)
#                 metadata.append(chunk)

#     return build_faiss_index(
#         embeddings
#     ), metadata


# def build_target_index(
#     embedded_chunks: list[dict]
# ):
#     """
#     Build index for target-language
#     sentence chunks.
#     """

#     embeddings = []
#     metadata = []

#     for chunk in embedded_chunks:

#         if (
#             chunk.get("chunk_type") == "sentence"
#             and chunk.get("chunk_id", "").startswith("tgt_")
#         ):

#             embedding = chunk.get("embedding")

#             if embedding:
#                 embeddings.append(embedding)
#                 metadata.append(chunk)

#     return build_faiss_index(
#         embeddings
#     ), metadata


# def build_terminology_index(
#     embedded_chunks: list[dict]
# ):
#     """
#     Build terminology index.
#     """

#     embeddings = []
#     metadata = []

#     for chunk in embedded_chunks:

#         if chunk.get("chunk_type") == "term":

#             embedding = chunk.get("embedding")

#             if embedding:
#                 embeddings.append(embedding)
#                 metadata.append(chunk)

#     return build_faiss_index(
#         embeddings
#     ), metadata


# def build_entity_index(
#     embedded_chunks: list[dict]
# ):
#     """
#     Build named-entity index.
#     """

#     embeddings = []
#     metadata = []

#     for chunk in embedded_chunks:

#         if chunk.get("chunk_type") == "named_entity":

#             embedding = chunk.get("embedding")

#             if embedding:
#                 embeddings.append(embedding)
#                 metadata.append(chunk)

#     return build_faiss_index(
#         embeddings
#     ), metadata


# def build_domain_index(
#     embedded_chunks: list[dict]
# ):
#     """
#     Build domain-document index.

#     Includes paragraph and section chunks.
#     """

#     embeddings = []
#     metadata = []

#     for chunk in embedded_chunks:

#         if chunk.get("chunk_type") in {
#             "paragraph",
#             "section"
#         }:

#             embedding = chunk.get("embedding")

#             if embedding:
#                 embeddings.append(embedding)
#                 metadata.append(chunk)

#     return build_faiss_index(
#         embeddings
#     ), metadata

# def build_parallel_index(
#     embedded_chunks: list[dict]
# ):
#     """
#     Build a FAISS index for parallel sentence pairs.

#     Each parallel pair contributes two vectors:
#         - source embedding
#         - target embedding

#     Both vectors share the same parallel chunk metadata,
#     so the source-target relationship is preserved.
#     """

#     embeddings = []
#     metadata = []

#     for chunk in embedded_chunks:

#         if chunk.get("chunk_type") != "parallel_sentence":
#             continue

#         source_embedding = chunk.get(
#             "source_embedding"
#         )

#         target_embedding = chunk.get(
#             "target_embedding"
#         )

#         # Add source vector
#         if source_embedding:

#             embeddings.append(
#                 source_embedding
#             )

#             metadata.append({
#                 **chunk,
#                 "embedding_side": "source"
#             })

#         # Add target vector
#         if target_embedding:

#             embeddings.append(
#                 target_embedding
#             )

#             metadata.append({
#                 **chunk,
#                 "embedding_side": "target"
#             })

#     return build_faiss_index(
#         embeddings
#     ), metadata


import faiss
import numpy as np
from pathlib import Path
import json


EMBEDDING_DIMENSION = 384


def build_faiss_index(embeddings: list[list[float]]):
    """
    Build a FAISS index using cosine similarity.
    """

    if not embeddings:
        return None

    vectors = np.array(
        embeddings,
        dtype="float32"
    )

    faiss.normalize_L2(vectors)

    index = faiss.IndexFlatIP(
        EMBEDDING_DIMENSION
    )

    index.add(vectors)

    return index


def save_index(
    index,
    metadata: list[dict],
    index_path: str | Path,
    metadata_path: str | Path
):
    """
    Save FAISS index and corresponding metadata.
    """

    if index is None:
        return

    index_path = Path(index_path)
    metadata_path = Path(metadata_path)

    index_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    faiss.write_index(
        index,
        str(index_path)
    )

    with open(
        metadata_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2
        )


def build_source_index(
    embedded_chunks: list[dict]
):
    embeddings = []
    metadata = []

    for chunk in embedded_chunks:

        if (
            chunk.get("chunk_type") == "sentence"
            and chunk.get("chunk_id", "").startswith("src_")
        ):

            embedding = chunk.get("embedding")

            if embedding:
                embeddings.append(embedding)
                metadata.append(chunk)

    return build_faiss_index(embeddings), metadata


def build_target_index(
    embedded_chunks: list[dict]
):
    embeddings = []
    metadata = []

    for chunk in embedded_chunks:

        if (
            chunk.get("chunk_type") == "sentence"
            and chunk.get("chunk_id", "").startswith("tgt_")
        ):

            embedding = chunk.get("embedding")

            if embedding:
                embeddings.append(embedding)
                metadata.append(chunk)

    return build_faiss_index(embeddings), metadata


def build_parallel_index(
    embedded_chunks: list[dict]
):
    """
    Build index for parallel sentence pairs.

    Both source and target embeddings are stored,
    while metadata keeps the pair relationship.
    """

    embeddings = []
    metadata = []

    for chunk in embedded_chunks:

        if chunk.get("chunk_type") != "parallel_sentence":
            continue

        source_embedding = chunk.get(
            "source_embedding"
        )

        target_embedding = chunk.get(
            "target_embedding"
        )

        if source_embedding:

            embeddings.append(
                source_embedding
            )

            metadata.append({
                **chunk,
                "embedding_side": "source"
            })

        if target_embedding:

            embeddings.append(
                target_embedding
            )

            metadata.append({
                **chunk,
                "embedding_side": "target"
            })

    return build_faiss_index(embeddings), metadata


def build_terminology_index(
    embedded_chunks: list[dict]
):
    embeddings = []
    metadata = []

    for chunk in embedded_chunks:

        if chunk.get("chunk_type") == "term":

            embedding = chunk.get("embedding")

            if embedding:
                embeddings.append(embedding)
                metadata.append(chunk)

    return build_faiss_index(embeddings), metadata


def build_entity_index(
    embedded_chunks: list[dict]
):
    embeddings = []
    metadata = []

    for chunk in embedded_chunks:

        if chunk.get("chunk_type") == "named_entity":

            embedding = chunk.get("embedding")

            if embedding:
                embeddings.append(embedding)
                metadata.append(chunk)

    return build_faiss_index(embeddings), metadata


def build_domain_index(
    embedded_chunks: list[dict]
):
    embeddings = []
    metadata = []

    for chunk in embedded_chunks:

        if chunk.get("chunk_type") in {
            "paragraph",
            "section"
        }:

            embedding = chunk.get("embedding")

            if embedding:
                embeddings.append(embedding)
                metadata.append(chunk)

    return build_faiss_index(embeddings), metadata

def build_indexes(
    embedded_chunks: list[dict],
    index_manager
):
    """
    Build and update all indexes using IndexManager.
    """

    return index_manager.build_all(
        embedded_chunks
    )