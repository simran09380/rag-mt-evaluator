from rank_bm25 import BM25Okapi


class BM25Retriever:
    """
    Lexical retrieval using BM25.
    """

    def __init__(self, chunks=None):

        self.chunks = []
        self.bm25 = None

        if chunks:
            self.build(chunks)

    def build(self, chunks: list[dict]):
        """
        Build BM25 index from chunks.
        """

        self.chunks = [
            chunk
            for chunk in chunks
            if self._get_text(chunk)
        ]

        tokenized_corpus = [
            self._get_text(chunk).lower().split()
            for chunk in self.chunks
        ]

        if not tokenized_corpus:
            self.bm25 = None
            return

        self.bm25 = BM25Okapi(
            tokenized_corpus
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> list[dict]:

        if (
            not query
            or not query.strip()
            or self.bm25 is None
        ):
            return []

        tokenized_query = (
            query.lower().split()
        )

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        results = []

        for index in ranked_indices[:top_k]:

            chunk = self.chunks[index]

            results.append({
                "chunk_id": chunk.get(
                    "chunk_id"
                ),
                "chunk_type": chunk.get(
                    "chunk_type"
                ),
                "text": self._get_text(
                    chunk
                ),
                "bm25_score": float(
                    scores[index]
                ),
                "metadata": chunk
            })

        return results

    @staticmethod
    def _get_text(chunk: dict) -> str:

        if chunk.get("text"):
            return chunk["text"]

        if chunk.get("source_text"):
            return chunk["source_text"]

        if chunk.get("target_text"):
            return chunk["target_text"]

        if chunk.get("term"):
            return chunk["term"]

        if chunk.get("entity"):
            return chunk["entity"]

        return ""