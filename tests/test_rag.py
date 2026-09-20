from app.retriever import search
from app.rag import build_context


def test_retriever_returns_results():
    results = search(
        "What are the characteristics of trustworthy AI?",
        top_k=5,
    )

    assert "documents" in results
    assert "metadatas" in results
    assert len(results["documents"][0]) == 5


def test_retriever_finds_correct_source():
    results = search(
        "What are the characteristics of trustworthy AI?",
        top_k=5,
    )

    sources = [
        metadata["source"]
        for metadata in results["metadatas"][0]
    ]

    assert "nist_ai_rmf.txt" in sources


def test_build_context_contains_source_information():
    results = search(
        "What are the characteristics of trustworthy AI?",
        top_k=3,
    )

    context = build_context(results)

    assert "Document:" in context
    assert "Chunk:" in context
    assert "nist_ai_rmf.txt" in context