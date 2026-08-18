from summarizer import parse_response
from summarizer import parse_response, summarize_article
import summarizer

def test_parse_response():
    response = """
SUMMARY:
This is a test summary.

WHY_IT_MATTERS:
This is why the article matters.
"""

    result = parse_response(response)

    assert result["summary"] == "This is a test summary."
    assert result["why_it_matters"] == "This is why the article matters."


def test_parse_response_without_why_it_matters():
    response = """
SUMMARY:
This is a test summary.
"""

    result = parse_response(response)

    assert result["summary"] == "This is a test summary."
    assert result["why_it_matters"] == ""


def test_parse_response_without_summary_marker():
    response = "This is just a plain response."

    result = parse_response(response)

    assert result["summary"] == "This is just a plain response."
    assert result["why_it_matters"] == ""


def test_parse_response_strips_whitespace():
    response = """
SUMMARY:

   This is a test summary.   

WHY_IT_MATTERS:

   This is why it matters.   
"""

    result = parse_response(response)

    assert result["summary"] == "This is a test summary."
    assert result["why_it_matters"] == "This is why it matters."


def test_summarize_article_uses_provided_content(monkeypatch):
    captured = {}

    def fake_generate_response(prompt, **kwargs):
        captured["prompt"] = prompt

        return """
SUMMARY:
Test summary.

WHY_IT_MATTERS:
Test significance.
"""

    monkeypatch.setattr(
        summarizer,
        "generate_response",
        fake_generate_response,
    )

    article = {
        "title": "Test Article",
        "category": "technology",
        "url": "https://example.com/article",
        "summary": "Original RSS summary.",
    }

    summarize_article(
        article,
        content="Actual article content.",
    )

    assert "Actual article content." in captured["prompt"]