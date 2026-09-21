from types import SimpleNamespace

from app.agent import run_agent


def test_agent_returns_answer(monkeypatch):

    fake_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="Trustworthy AI should be valid and reliable.",
                    tool_calls=None,
                )
            )
        ]
    )

    monkeypatch.setattr(
        "app.agent.client.chat.completions.create",
        lambda **kwargs: fake_response,
    )

    result = run_agent(
        "What are the characteristics of trustworthy AI?"
    )

    assert "answer" in result
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0


def test_agent_uses_tool(monkeypatch):

    tool_call = SimpleNamespace(
        id="test-tool-call",
        function=SimpleNamespace(
            name="search_documents",
            arguments='{"query": "trustworthy AI", "top_k": 3}',
        ),
    )

    first_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=None,
                    tool_calls=[tool_call],
                )
            )
        ]
    )

    second_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="Trustworthy AI should be valid and reliable.",
                    tool_calls=None,
                )
            )
        ]
    )

    responses = iter([
        first_response,
        second_response,
    ])

    monkeypatch.setattr(
        "app.agent.client.chat.completions.create",
        lambda **kwargs: next(responses),
    )

    fake_tool_result = {
        "query": "trustworthy AI",
        "results": [
            {
                "source": "nist_ai_rmf.txt",
                "chunk": 32,
                "distance": 0.1,
                "text": "Trustworthy AI information.",
            }
        ],
    }

    monkeypatch.setattr(
        "app.agent.search_documents",
        lambda query, top_k: fake_tool_result,
    )

    result = run_agent(
        "What are the characteristics of trustworthy AI?"
    )

    assert result["tool_used"] is True
    assert len(result["tool_results"]) == 1
    assert result["tool_results"][0]["results"][0]["source"] == (
        "nist_ai_rmf.txt"
    )