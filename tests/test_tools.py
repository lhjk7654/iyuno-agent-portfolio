from app.tools import search_documents


def test_search_documents_tool():
    result = search_documents(
        "What are the characteristics of trustworthy AI?",
        top_k=3,
    )

    assert "query" in result
    assert "results" in result
    assert len(result["results"]) == 3


def test_search_documents_returns_source():
    result = search_documents(
        "What are the characteristics of trustworthy AI?",
        top_k=5,
    )

    sources = [
        item["source"]
        for item in result["results"]
    ]

    assert "nist_ai_rmf.txt" in sources