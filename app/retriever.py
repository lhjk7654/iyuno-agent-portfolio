from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR = Path("data/chroma")
COLLECTION_NAME = "iyuno_documents"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_collection(name=COLLECTION_NAME)


def search(query: str, top_k: int = 5):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
    )

    return results


def main():
    query = input("질문을 입력하세요: ")
    results = search(query)

    print("\n=== Search Results ===")

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1,
    ):
        print(f"\n[Result {i}]")
        print(f"Source: {metadata['source']}")
        print(f"Chunk: {metadata['chunk_index']}")
        print(f"Distance: {distance:.4f}")
        print("-" * 60)
        print(document[:500])


if __name__ == "__main__":
    main()