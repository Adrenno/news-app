from processor import (
    clean_text,
    normalize_title,
    normalize_article,
    deduplicate_articles,
    create_article,
)


def test_clean_text():
    text = "  Hello   <b>world</b> &amp; everyone  "

    result = clean_text(text)

    assert result == "Hello world & everyone"


def test_normalize_title():
    title = "Breaking News: AI's Big Impact!"

    result = normalize_title(title)

    assert result == "breaking news ais big impact"


def test_normalize_article():
    article = {
        "title": "  Test Article  ",
        "url": "https://example.com/article",
        "summary": "  A test summary  ",
        "category": "Technology",
        "source": "Test Source",
    }

    result = normalize_article(article)

    assert result["title"] == "Test Article"
    assert result["summary"] == "A test summary"
    assert result["normalized_title"] == "test article"

    # normalize_article should preserve the URL
    assert result["url"] == "https://example.com/article"


def test_deduplicate_articles():
    articles = [
        {
            "title": "Article One",
            "normalized_title": "article one",
        },
        {
            "title": "Article One Duplicate",
            "normalized_title": "article one",
        },
        {
            "title": "Article Two",
            "normalized_title": "article two",
        },
    ]

    result = deduplicate_articles(articles)

    assert len(result) == 2
    assert result[0]["title"] == "Article One"
    assert result[1]["title"] == "Article Two"


def test_create_article():
    result = create_article(
        title="  Test Article  ",
        url="  https://example.com/article  ",
        published="2026-08-12",
        summary="  Test summary  ",
        source="Test Source",
        category="Technology",
    )

    assert result["title"] == "Test Article"
    assert result["url"] == "https://example.com/article"
    assert result["published"] == "2026-08-12"
    assert result["summary"] == "Test summary"
    assert result["source"] == "Test Source"
    assert result["category"] == "Technology"
    assert result["score"] == 0.0