from app.retrieval.retrieval_service import RetrievalService
from app.reranking.reranker import Reranker


class QueryRetrievalService:
    """
    Connect:

    Module 3: Query Generation
            ↓
    Module 5: Hybrid Retrieval
            ↓
    Module 6: Retrieval Reranking
    """

    def __init__(
        self,
        chunks: list[dict],
        index_manager
    ):
        # --------------------------------------
        # Module 5
        # --------------------------------------

        self.retrieval_service = RetrievalService(
            chunks=chunks,
            index_manager=index_manager
        )

        # --------------------------------------
        # Module 6
        # --------------------------------------

        self.reranker = Reranker()

    def retrieve_generated_queries(
        self,
        generated_queries: dict,
        source_text: str,
        mt_output: str,
        source_lang: str | None = None,
        target_lang: str | None = None,
        query_terms: list[str] | None = None,
        query_entities: list[str] | None = None,
        query_metadata: dict | None = None,
        index_type: str = "source",
        top_k: int = 5,
        retrieval_top_k: int = 20
    ) -> dict:
        """
        Retrieve candidates using Module 5 and
        rerank them using Module 6.

        retrieval_top_k:
            Number of candidates retrieved by Module 5.

        top_k:
            Number of final evidence pieces returned
            after Module 6 reranking.
        """

        results = {}

        # ======================================
        # PROCESS EACH GENERATED QUERY TYPE
        # ======================================

        for query_type, query in generated_queries.items():

            # ==================================
            # LIST OF QUERIES
            # ==================================

            if isinstance(query, list):

                query_results = []

                for single_query in query:

                    # Ignore non-string values
                    if not isinstance(
                        single_query,
                        str
                    ):
                        continue

                    if not single_query.strip():
                        continue

                    # ------------------------------
                    # MODULE 5: RETRIEVAL
                    # ------------------------------

                    retrieved = (
                        self.retrieval_service.retrieve(
                            query=single_query,
                            query_metadata=query_metadata,
                            index_type=index_type,
                            top_k=retrieval_top_k
                        )
                    )

                    # ------------------------------
                    # MODULE 6: RERANKING
                    # ------------------------------

                    reranked = self.reranker.rerank(
                        source_text=source_text,
                        hypothesis_text=mt_output,
                        candidates=retrieved,
                        source_lang=source_lang,
                        target_lang=target_lang,
                        query_terms=query_terms,
                        query_entities=query_entities,
                        top_k=top_k
                    )

                    query_results.append({
                        "query": single_query,
                        "results": reranked
                    })

                results[query_type] = query_results

            # ==================================
            # SINGLE QUERY
            # ==================================

            elif isinstance(query, str):

                if not query.strip():
                    continue

                # ------------------------------
                # MODULE 5: RETRIEVAL
                # ------------------------------

                retrieved = (
                    self.retrieval_service.retrieve(
                        query=query,
                        query_metadata=query_metadata,
                        index_type=index_type,
                        top_k=retrieval_top_k
                    )
                )

                # ------------------------------
                # MODULE 6: RERANKING
                # ------------------------------

                reranked = self.reranker.rerank(
                    source_text=source_text,
                    hypothesis_text=mt_output,
                    candidates=retrieved,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    query_terms=query_terms,
                    query_entities=query_entities,
                    top_k=top_k
                )

                results[query_type] = {
                    "query": query,
                    "results": reranked
                }

            # ==================================
            # IGNORE OTHER TYPES
            # ==================================

            else:
                continue

        return results