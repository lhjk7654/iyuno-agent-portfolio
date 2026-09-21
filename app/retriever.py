from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


DB_DIR = Path("data/chroma")
COLLECTION_NAME = "iyuno_documents"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

client = chromadb.PersistentClient(path=str(DB_DIR))


def search(query: str, top_k: int = 5):
    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    query_embedding = model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
    )

    return results