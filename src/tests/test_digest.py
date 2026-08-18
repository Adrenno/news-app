from digest import (
    clean_summary,
    group_by_category,
    filter_important_articles,
    generate_digest,
)


def test_clean_summary():
    summary = "  This is <b>important</b> news. &amp; more.  "

    result = clean_summary(summary)

    assert result == "This is important news. & more."


def test_group_by_category():
    articles = [
        {
            "title": "Taiwan News",
            "category": "taiwan",
        },
        {
            "title": "World News",
            "category": "world",
        },
        {
            "title": "Another Taiwan News",
            "category": "taiwan",
        },
    ]

    result = group_by_category(articles)

    assert len(result["taiwan"]) == 2
    assert len(result["world"]) == 1

    assert result["taiwan"][0]["title"] == "Taiwan News"
    assert result["taiwan"][1]["title"] == "Another Taiwan News"


def test_filter_important_articles():
    articles = [
        {
            "title": "Important",
            "score": 20,
        },
        {
            "title": "Exactly Minimum",
            "score": 12,
        },
        {
            "title": "Not Important",
            "score": 11,
        },
    ]

    result = filter_important_articles(articles)

    assert len(result) == 2
    assert result[0]["title"] == "Important"
    assert result[1]["title"] == "Exactly Minimum"


def test_generate_digest_category_order():
    articles = [
        {
            "title": "Technology News",
            "category": "technology",
            "summary": "Technology summary.",
            "url": "https://example.com/technology",
            "source": "Test Source",
            "score": 20,
        },
        {
            "title": "Taiwan News",
            "category": "taiwan",
            "summary": "Taiwan summary.",
            "url": "https://example.com/taiwan",
            "source": "Test Source",
            "score": 20,
        },
        {
            "title": "World News",
            "category": "world",
            "summary": "World summary.",
            "url": "https://example.com/world",
            "source": "Test Source",
            "score": 20,
        },
    ]

    result = generate_digest(articles)

    titles = [
        article["title"]
        for article in result["articles"]
    ]

    assert titles == [
        "Taiwan News",
        "World News",
        "Technology News",
    ]


def test_generate_digest_limits_articles_per_category():
    articles = [
        {
            "title": f"Technology News {i}",
            "category": "technology",
            "summary": f"Summary {i}.",
            "url": f"https://example.com/{i}",
            "source": "Test Source",
            "score": 20,
        }
        for i in range(5)
    ]

    result = generate_digest(
        articles,
        articles_per_category=3,
    )

    assert len(result["articles"]) == 3
    assert [
        article["title"]
        for article in result["articles"]
    ] == [
        "Technology News 0",
        "Technology News 1",
        "Technology News 2",
    ]