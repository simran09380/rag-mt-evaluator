# from pathlib import Path

# from .index_builder import (
#     build_source_index,
#     build_target_index,
#     build_parallel_index,
#     build_terminology_index,
#     build_entity_index,
#     build_domain_index,
#     save_index,
# )


# # Directory where all FAISS indexes will be stored
# INDEX_DIR = Path("indexes")


# def build_all_indexes(
#     embedded_chunks: list[dict],
#     index_dir: str | Path = INDEX_DIR
# ) -> dict:
#     """
#     Build and save all available Module 4 indexes.

#     Indexes:
#         1. Source-language passages
#         2. Target-language passages
#         3. Terminology
#         4. Named entities
#         5. Domain documents

#     Parallel index will be handled separately because
#     parallel chunks contain source_embedding and
#     target_embedding.
#     """

#     index_dir = Path(index_dir)

#     results = {}

#     # --------------------------------------------------
#     # 1. SOURCE-LANGUAGE INDEX
#     # --------------------------------------------------

#     source_index, source_metadata = build_source_index(
#         embedded_chunks
#     )

#     if source_index is not None:

#         save_index(
#             index=source_index,
#             metadata=source_metadata,
#             index_path=index_dir / "source" / "index.faiss",
#             metadata_path=index_dir / "source" / "metadata.json"
#         )

#         results["source"] = {
#             "status": "created",
#             "vectors": source_index.ntotal
#         }

#     else:

#         results["source"] = {
#             "status": "empty",
#             "vectors": 0
#         }

#     # --------------------------------------------------
#     # 2. TARGET-LANGUAGE INDEX
#     # --------------------------------------------------

#     target_index, target_metadata = build_target_index(
#         embedded_chunks
#     )

#     if target_index is not None:

#         save_index(
#             index=target_index,
#             metadata=target_metadata,
#             index_path=index_dir / "target" / "index.faiss",
#             metadata_path=index_dir / "target" / "metadata.json"
#         )

#         results["target"] = {
#             "status": "created",
#             "vectors": target_index.ntotal
#         }

#     else:

#         results["target"] = {
#             "status": "empty",
#             "vectors": 0
#         }

#         # --------------------------------------------------
#     # 3. PARALLEL SENTENCE INDEX
#     # --------------------------------------------------

#     parallel_index, parallel_metadata = (
#         build_parallel_index(
#             embedded_chunks
#         )
#     )

#     if parallel_index is not None:

#         save_index(
#             index=parallel_index,
#             metadata=parallel_metadata,
#             index_path=index_dir / "parallel" / "index.faiss",
#             metadata_path=index_dir / "parallel" / "metadata.json"
#         )

#         results["parallel"] = {
#             "status": "created",
#             "vectors": parallel_index.ntotal
#         }

#     else:

#         results["parallel"] = {
#             "status": "empty",
#             "vectors": 0
#         }

#     # --------------------------------------------------
#     # 3. TERMINOLOGY INDEX
#     # --------------------------------------------------

#     terminology_index, terminology_metadata = (
#         build_terminology_index(
#             embedded_chunks
#         )
#     )

#     if terminology_index is not None:

#         save_index(
#             index=terminology_index,
#             metadata=terminology_metadata,
#             index_path=index_dir / "terminology" / "index.faiss",
#             metadata_path=index_dir / "terminology" / "metadata.json"
#         )

#         results["terminology"] = {
#             "status": "created",
#             "vectors": terminology_index.ntotal
#         }

#     else:

#         results["terminology"] = {
#             "status": "empty",
#             "vectors": 0
#         }

#     # --------------------------------------------------
#     # 4. NAMED ENTITY INDEX
#     # --------------------------------------------------

#     entity_index, entity_metadata = build_entity_index(
#         embedded_chunks
#     )

#     if entity_index is not None:

#         save_index(
#             index=entity_index,
#             metadata=entity_metadata,
#             index_path=index_dir / "entities" / "index.faiss",
#             metadata_path=index_dir / "entities" / "metadata.json"
#         )

#         results["entities"] = {
#             "status": "created",
#             "vectors": entity_index.ntotal
#         }

#     else:

#         results["entities"] = {
#             "status": "empty",
#             "vectors": 0
#         }

#     # --------------------------------------------------
#     # 5. DOMAIN DOCUMENT INDEX
#     # --------------------------------------------------

#     domain_index, domain_metadata = build_domain_index(
#         embedded_chunks
#     )

#     if domain_index is not None:

#         save_index(
#             index=domain_index,
#             metadata=domain_metadata,
#             index_path=index_dir / "domain" / "index.faiss",
#             metadata_path=index_dir / "domain" / "metadata.json"
#         )

#         results["domain"] = {
#             "status": "created",
#             "vectors": domain_index.ntotal
#         }

#     else:

#         results["domain"] = {
#             "status": "empty",
#             "vectors": 0
#         }

#     return results

import faiss
import json
from pathlib import Path

from .index_builder import (
    build_source_index,
    build_target_index,
    build_parallel_index,
    build_terminology_index,
    build_entity_index,
    build_domain_index,
)


class IndexManager:
    """
    Manage all FAISS indexes used by the RAG-MTE system.
    """

    def __init__(
        self,
        index_dir: str = "indexes"
    ):

        self.index_dir = Path(index_dir)

        self.indexes = {}
        self.metadata = {}

        self.index_types = [
            "source",
            "target",
            "parallel",
            "terminology",
            "entities",
            "domain",
        ]

        self.load_indexes()

    # ==================================================
    # LOAD EXISTING INDEXES
    # ==================================================

    def load_indexes(self):
        """
        Load previously saved indexes and metadata.
        """

        for index_type in self.index_types:

            index_path = (
                self.index_dir
                / index_type
                / "index.faiss"
            )

            metadata_path = (
                self.index_dir
                / index_type
                / "metadata.json"
            )

            if (
                index_path.exists()
                and metadata_path.exists()
            ):

                self.indexes[index_type] = (
                    faiss.read_index(
                        str(index_path)
                    )
                )

                with open(
                    metadata_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.metadata[index_type] = (
                        json.load(file)
                    )

    # ==================================================
    # ADD VECTORS
    # ==================================================

    def add_index(
        self,
        index_type: str,
        new_index,
        new_metadata: list[dict]
    ):
        """
        Add newly generated vectors to an
        existing index.
        """

        if new_index is None:
            return

        if index_type in self.indexes:

            self.indexes[index_type].add(
                new_index.reconstruct_n(
                    0,
                    new_index.ntotal
                )
            )

            self.metadata[index_type].extend(
                new_metadata
            )

        else:

            self.indexes[index_type] = (
                new_index
            )

            self.metadata[index_type] = (
                new_metadata
            )

        self.save_index(index_type)

    # ==================================================
    # SAVE INDEX
    # ==================================================

    def save_index(
        self,
        index_type: str
    ):
        """
        Save FAISS index and metadata.
        """

        directory = (
            self.index_dir / index_type
        )

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.indexes[index_type],
            str(directory / "index.faiss")
        )

        with open(
            directory / "metadata.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.metadata[index_type],
                file,
                ensure_ascii=False,
                indent=2
            )

    # ==================================================
    # BUILD ALL INDEXES
    # ==================================================

    def build_all(
        self,
        embedded_chunks: list[dict]
    ):
        """
        Build/update all six indexes.
        """

        results = {}

        builders = {
            "source": build_source_index,
            "target": build_target_index,
            "parallel": build_parallel_index,
            "terminology": build_terminology_index,
            "entities": build_entity_index,
            "domain": build_domain_index,
        }

        for index_type, builder in builders.items():

            index, metadata = builder(
                embedded_chunks
            )

            self.add_index(
                index_type,
                index,
                metadata
            )

            results[index_type] = {
                "vectors_added": (
                    len(metadata)
                ),
                "total_vectors": (
                    self.indexes[index_type].ntotal
                    if index_type in self.indexes
                    else 0
                )
            }

        return results