from app.agent import run_agent


def test_agent_returns_answer():
    result = run_agent(
        "What are the characteristics of trustworthy AI?"
    )

    assert "answer" in result
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0


def test_agent_uses_tool():
    result = run_agent(
        "What are the characteristics of trustworthy AI?"
    )

    assert result["tool_used"] is True
    assert len(result["tool_results"]) > 0