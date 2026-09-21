from app.rag import build_context


def test_build_context_contains_source_information():
    results = {
        "documents": [[
            "Trustworthy AI should be valid and reliable.",
            "AI systems should be safe and secure.",
            "AI systems should be accountable and transparent.",
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
    }

    context = build_context(results)

    assert "Document:" in context
    assert "Chunk:" in context
    assert "nist_ai_rmf.txt" in context
    assert "nist_csf_2_0.txt" in context