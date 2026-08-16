from sentence_transformers import SentenceTransformer


semantic_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


multilingual_model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)