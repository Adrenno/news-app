from ranking import (
    recency_score,
    category_score,
    keyword_score,
    source_score,
    calculate_score,
    rank_articles,
)


def test_recency_score():
    assert recency_score("") == 0
    assert recency_score("not a valid date") == 0


def test_category_score():
    assert category_score("programming") == 10
    assert category_score("technology") == 8
    assert category_score("business") == 7
    assert category_score("world") == 6
    assert category_score("unknown") == 0


def test_keyword_score():
    title = "Python and AI programming news"

    result = keyword_score(title)

    assert result == (
        5 + 5 + 4
    )


def test_keyword_score_is_case_insensitive():
    assert keyword_score("PYTHON AI") == 10


def test_source_score():
    assert source_score("BBC World") == 3
    assert source_score("BBC Technology") == 3
    assert source_score("Unknown Source") == 0


def test_calculate_score():
    article = {
        "published": "",
        "category": "programming",
        "title": "Python programming news",
        "source": "BBC Technology",
    }

    result = calculate_score(article)

    assert result["recency"] == 0
    assert result["category"] == 10
    assert result["keywords"] == 9
    assert result["source"] == 3
    assert result["total"] == 22


def test_rank_articles():
    articles = [
        {
            "title": "World News",
            "category": "world",
            "source": "BBC World",
            "published": "",
        },
        {
            "title": "Python Programming News",
            "category": "programming",
            "source": "BBC Technology",
            "published": "",
        },
        {
            "title": "Business News",
            "category": "business",
            "source": "BBC Business",
            "published": "",
        },
    ]

    result = rank_articles(articles)

    assert result[0]["title"] == "Python Programming News"
    assert result[1]["title"] == "Business News"
    assert result[2]["title"] == "World News"


def test_rank_articles_includes_ranking_details():
    article = {
        "title": "Python News",
        "category": "programming",
        "source": "BBC Technology",
        "published": "",
    }

    result = rank_articles([article])

    ranked_article = result[0]

    assert "score" in ranked_article
    assert "ranking_details" in ranked_article

    assert ranked_article["ranking_details"] == {
        "recency": 0,
        "category": 10,
        "keywords": 5,
        "source": 3,
    }