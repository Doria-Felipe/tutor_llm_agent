import chromadb
from src.embeddings.model import get_model

client = chromadb.PersistentClient(path="./chroma_easy_german")

col = client.get_or_create_collection(
    "easy_german_a1_multi",
    metadata={"hnsw:space": "cosine"}
)

_model = get_model()