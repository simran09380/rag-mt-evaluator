from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.dense_retriever import DenseRetriever
from app.retrieval.metadata_scorer import MetadataScorer
from app.retrieval.authority_scorer import AuthorityScorer
from app.retrieval.hybrid_retriever import HybridRetriever


class RetrievalService:
    """
    Main orchestration layer for Module 5.

    Combines:
        - BM25 retrieval
        - Dense retrieval
        - Metadata scoring
        - Authority scoring
        - Hybrid ranking
    """

    def __init__(
        self,
        chunks: list[dict],
        index_manager
    ):

        # -----------------------------------------
        # Retrieval components
        # -----------------------------------------

        self.bm25_retriever = BM25Retriever(
            chunks
        )

        self.dense_retriever = DenseRetriever(
            index_manager
        )

        self.metadata_scorer = MetadataScorer()

        self.authority_scorer = AuthorityScorer()

        # -----------------------------------------
        # Hybrid retriever
        # -----------------------------------------

        self.hybrid_retriever = HybridRetriever(
            bm25_retriever=self.bm25_retriever,
            dense_retriever=self.dense_retriever,
            metadata_scorer=self.metadata_scorer,
            authority_scorer=self.authority_scorer
        )

    def retrieve(
        self,
        query: str,
        query_metadata: dict | None = None,
        index_type: str = "source",
        top_k: int = 5
    ) -> list[dict]:
        """
        Retrieve the most relevant chunks
        for a query.
        """

        return self.hybrid_retriever.retrieve(
            query=query,
            query_metadata=query_metadata,
            index_type=index_type,
            top_k=top_k
        )