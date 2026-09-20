from pathlib import Path

from pypdf import PdfReader


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def extract_pdf(pdf_path: Path) -> Path:
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append(
            f"\n--- PAGE {page_number} ---\n{text}"
        )

    output_path = PROCESSED_DIR / f"{pdf_path.stem}.txt"
    output_path.write_text(
        "\n".join(pages),
        encoding="utf-8",
    )

    print(f"Extracted: {pdf_path.name}")
    print(f"Pages: {len(reader.pages)}")
    print(f"Saved: {output_path}")

    return output_path


def main() -> None:
    pdf_files = list(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    for pdf_file in pdf_files:
        extract_pdf(pdf_file)


if __name__ == "__main__":
    main()