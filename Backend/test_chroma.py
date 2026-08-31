from app.indexing.index_manager import IndexManager


manager = IndexManager()

collection = manager.get_index("source")

print("Documents:", collection.count())

data = collection.get(
    include=["documents", "metadatas"]
)

print("\nIDs:")
print(data["ids"])

print("\nDocuments:")
print(data["documents"])

print("\nMetadata:")
print(data["metadatas"])