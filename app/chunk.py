from pathlib import Path
import json


PROCESSED_DIR = Path("data/processed")
CHUNK_DIR = Path("data/chunks")

CHUNK_DIR.mkdir(parents=True, exist_ok=True)


CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def split_text(text: str) -> list[str]:
    chunks = []

    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def process_file(file_path: Path) -> Path:
    text = file_path.read_text(encoding="utf-8")

    chunks = split_text(text)

    records = []

    for index, chunk in enumerate(chunks):
        records.append(
            {
                "id": f"{file_path.stem}-{index}",
                "source": file_path.name,
                "chunk_index": index,
                "text": chunk,
            }
        )

    output_path = CHUNK_DIR / f"{file_path.stem}.json"

    output_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"File: {file_path.name}")
    print(f"Chunks: {len(records)}")
    print(f"Saved: {output_path}")

    return output_path


def main() -> None:
    files = list(PROCESSED_DIR.glob("*.txt"))

    if not files:
        print("No processed text files found.")
        return

    for file_path in files:
        process_file(file_path)


if __name__ == "__main__":
    main()