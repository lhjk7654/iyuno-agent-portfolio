from app.tools import search_documents


def test_search_documents_tool(monkeypatch):
    fake_results = {
        "documents": [[
            "Trustworthy AI is valid and reliable.",
            "AI systems should be safe.",
            "AI systems should be accountable.",
        ]],
        "metadatas": [[
            {
                "source": "nist_ai_rmf.txt",
                "chunk_index": 32,
            },
            {
                "source": "nist_ai_rmf.txt",
                "chunk_index": 31,
            },
            {
                "source": "nist_csf_2_0.txt",
                "chunk_index": 10,
            },
        ]],
        "distances": [[
            0.1,
            0.2,
            0.3,
        ]],
    }

    monkeypatch.setattr(
        "app.tools.search",
        lambda query, top_k: fake_results,
    )

    result = search_documents(
        "What are the characteristics of trustworthy AI?",
        top_k=3,
    )

    assert result["query"] == (
        "What are the characteristics of trustworthy AI?"
    )

    assert len(result["results"]) == 3


def test_search_documents_returns_source(monkeypatch):
    fake_results = {
        "documents": [[
            "Trustworthy AI information.",
        ]],
        "metadatas": [[
            {
                "source": "nist_ai_rmf.txt",
                "chunk_index": 32,
            },
        ]],
        "distances": [[
            0.1,
        ]],
    }

    monkeypatch.setattr(
        "app.tools.search",
        lambda query, top_k: fake_results,
    )

    result = search_documents(
        "trustworthy AI",
        top_k=1,
    )

    assert result["results"][0]["source"] == "nist_ai_rmf.txt"