from app.retrieval.retrieval_service import RetrievalService


class QueryRetrievalService:
    """
    Connect Module 3 Query Generation
    with Module 5 Hybrid Retrieval.
    """

    def __init__(
        self,
        chunks: list[dict],
        index_manager
    ):
        self.retrieval_service = RetrievalService(
            chunks=chunks,
            index_manager=index_manager
        )

    def retrieve_generated_queries(
        self,
        generated_queries: dict,
        query_metadata: dict | None = None,
        index_type: str = "source",
        top_k: int = 5
    ) -> dict:

        results = {}

        for query_type, query in generated_queries.items():

            # --------------------------------------
            # LIST OF QUERIES
            # --------------------------------------
            if isinstance(query, list):

                query_results = []

                for single_query in query:

                    # Ignore non-string values
                    if not isinstance(single_query, str):
                        continue

                    if not single_query.strip():
                        continue

                    retrieved = self.retrieval_service.retrieve(
                        query=single_query,
                        query_metadata=query_metadata,
                        index_type=index_type,
                        top_k=top_k
                    )

                    query_results.append({
                        "query": single_query,
                        "results": retrieved
                    })

                results[query_type] = query_results

            # --------------------------------------
            # SINGLE QUERY
            # --------------------------------------
            elif isinstance(query, str):

                if not query.strip():
                    continue

                results[query_type] = {
                    "query": query,
                    "results": self.retrieval_service.retrieve(
                        query=query,
                        query_metadata=query_metadata,
                        index_type=index_type,
                        top_k=top_k
                    )
                }

            # --------------------------------------
            # IGNORE OTHER TYPES
            # --------------------------------------
            else:
                continue

        return results