import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


CHUNK_DIR = Path("data/chunks")
DB_DIR = Path("data/chroma")


def main() -> None:
    print("Loading embedding model...")

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(
        path=str(DB_DIR)
    )

    collection = client.get_or_create_collection(
        name="iyuno_documents"
    )

    json_files = list(CHUNK_DIR.glob("*.json"))

    if not json_files:
        print("No chunk files found.")
        return

    total = 0

    for json_file in json_files:
        print(f"Processing: {json_file.name}")

        records = json.loads(
            json_file.read_text(encoding="utf-8")
        )

        ids = [record["id"] for record in records]
        documents = [record["text"] for record in records]

        metadatas = [
            {
                "source": record["source"],
                "chunk_index": record["chunk_index"],
            }
            for record in records
        ]

        embeddings = model.encode(
            documents,
            show_progress_bar=True,
        ).tolist()

        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

        total += len(records)

    print()
    print("=== Embedding Summary ===")
    print(f"Documents processed: {len(json_files)}")
    print(f"Chunks stored: {total}")
    print(f"Vector DB: {DB_DIR}")


if __name__ == "__main__":
    main()