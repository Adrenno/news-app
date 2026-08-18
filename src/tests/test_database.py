import pytest
import os
import database


@pytest.fixture
def test_database(monkeypatch):
    test_database_url = os.getenv(
        "TEST_DATABASE_URL"
    )

    if not test_database_url:
        pytest.fail(
            "TEST_DATABASE_URL is not configured."
        )

    monkeypatch.setenv(
        "DATABASE_URL",
        test_database_url,
    )

    database.initialize_database()

    connection = database.get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                TRUNCATE TABLE
                    digest_articles,
                    digests,
                    articles
                RESTART IDENTITY CASCADE
            """)

        connection.commit()

    finally:
        connection.close()


def test_initialize_database(monkeypatch):
    test_database_url = os.getenv(
        "TEST_DATABASE_URL"
    )

    if not test_database_url:
        pytest.fail(
            "TEST_DATABASE_URL is not configured."
        )

    monkeypatch.setenv(
        "DATABASE_URL",
        test_database_url,
    )

    database.initialize_database()

    connection = database.get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """)

            tables = {
                row["table_name"]
                for row in cursor.fetchall()
            }

    finally:
        connection.close()

    assert "articles" in tables
    assert "digests" in tables
    assert "digest_articles" in tables

def test_save_and_get_top_articles(test_database):

    articles = [
        {
            "title": "Low Score Article",
            "url": "https://example.com/low",
            "published": "2026-08-12",
            "summary": "Low score.",
            "source": "Test Source",
            "category": "technology",
            "score": 5,
        },
        {
            "title": "High Score Article",
            "url": "https://example.com/high",
            "published": "2026-08-12",
            "summary": "High score.",
            "source": "Test Source",
            "category": "technology",
            "score": 20,
        },
    ]

    database.save_articles(articles)

    result = database.get_top_articles()

    assert len(result) == 2
    assert result[0]["title"] == "High Score Article"
    assert result[1]["title"] == "Low Score Article"

def test_get_top_articles_limit(test_database):

    articles = []

    for index in range(5):
        articles.append({
            "title": f"Article {index}",
            "url": f"https://example.com/{index}",
            "published": "2026-08-12",
            "summary": "Test summary.",
            "source": "Test Source",
            "category": "technology",
            "score": index,
        })

    database.save_articles(articles)

    result = database.get_top_articles(limit=2)

    assert len(result) == 2
    assert result[0]["score"] == 4
    assert result[1]["score"] == 3

def test_save_articles_updates_existing_url(test_database):

    original = {
        "title": "Original Title",
        "url": "https://example.com/article",
        "published": "2026-08-12",
        "summary": "Original summary.",
        "source": "Test Source",
        "category": "technology",
        "score": 5,
    }

    updated = {
        **original,
        "title": "Updated Title",
        "summary": "Updated summary.",
        "score": 20,
    }

    database.save_articles([original])
    database.save_articles([updated])

    result = database.get_top_articles()

    assert len(result) == 1
    assert result[0]["title"] == "Updated Title"
    assert result[0]["summary"] == "Updated summary."
    assert result[0]["score"] == 20

def test_digest_record(test_database):

    assert database.get_last_digest_time() is None

    articles = [
        {
            "title": "Test Article",
            "url": "https://example.com/test",
            "published": None,
            "summary": "Test summary",
            "source": "Test Source",
            "category": "technology",
            "score": 10,
        }
    ]

    database.save_articles(articles)

    saved_articles = database.get_top_articles()

    digest_id = database.create_digest_record(
        saved_articles
    )

    assert digest_id is not None

    result = database.get_last_digest_time()

    assert result is not None

def test_get_recent_articles(test_database):

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO articles (
            title,
            url,
            published,
            summary,
            source,
            category,
            score,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        "Recent Article",
        "https://example.com/recent",
        "2026-08-12",
        "Recent summary.",
        "Test Source",
        "technology",
        10,
        "2099-01-01 00:00:00",
    ))

    cursor.execute("""
        INSERT INTO articles (
            title,
            url,
            published,
            summary,
            source,
            category,
            score,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        "Old Article",
        "https://example.com/old",
        "2026-08-12",
        "Old summary.",
        "Test Source",
        "technology",
        20,
        "2000-01-01 00:00:00",
    ))

    connection.commit()
    connection.close()

    result = database.get_recent_articles(hours=3)

    assert len(result) == 1
    assert result[0]["title"] == "Recent Article"

def test_get_articles_since(test_database):

    connection = database.get_connection()
    cursor = connection.cursor()

    articles = [
        (
            "Old Article",
            "https://example.com/old",
            "2026-08-12",
            "Old summary.",
            "Test Source",
            "technology",
            5,
            "2026-08-12 10:00:00",
        ),
        (
            "New Article",
            "https://example.com/new",
            "2026-08-12",
            "New summary.",
            "Test Source",
            "technology",
            10,
            "2026-08-12 12:00:00",
        ),
    ]

    cursor.executemany("""
        INSERT INTO articles (
            title,
            url,
            published,
            summary,
            source,
            category,
            score,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, articles)

    connection.commit()
    connection.close()

    result = database.get_articles_since(
        "2026-08-12 11:00:00"
    )

    assert len(result) == 1
    assert result[0]["title"] == "New Article"

def test_get_digests(test_database):

    articles = [
        {
            "title": "First Article",
            "url": "https://example.com/first",
            "published": None,
            "summary": "First summary",
            "source": "Test Source",
            "category": "technology",
            "score": 10,
        },
        {
            "title": "Second Article",
            "url": "https://example.com/second",
            "published": None,
            "summary": "Second summary",
            "source": "Test Source",
            "category": "technology",
            "score": 20,
        },
    ]

    database.save_articles(articles)

    saved_articles = database.get_top_articles()

    database.create_digest_record(
        saved_articles
    )

    database.create_digest_record(
        saved_articles
    )

    digests = database.get_digests()

    assert len(digests) == 2

    assert len(digests[0]["articles"]) == 2
    assert len(digests[1]["articles"]) == 2

    assert (
        digests[0]["articles"][0]["title"]
        == "Second Article"
    )

def test_get_articles(test_database):

    articles = [
        {
            "title": "Technology Article",
            "url": "https://example.com/technology",
            "published": None,
            "summary": "Technology summary",
            "source": "BBC",
            "category": "technology",
            "score": 20,
        },
        {
            "title": "Business Article",
            "url": "https://example.com/business",
            "published": None,
            "summary": "Business summary",
            "source": "BBC",
            "category": "business",
            "score": 10,
        },
    ]

    database.save_articles(articles)

    result = database.get_articles()

    assert len(result) == 2
    assert result[0]["title"] == "Technology Article"
    assert result[1]["title"] == "Business Article"

def test_get_articles_filters_by_category(test_database):

    articles = [
        {
            "title": "Technology Article",
            "url": "https://example.com/technology",
            "published": None,
            "summary": "Technology summary",
            "source": "BBC",
            "category": "technology",
            "score": 20,
        },
        {
            "title": "Business Article",
            "url": "https://example.com/business",
            "published": None,
            "summary": "Business summary",
            "source": "BBC",
            "category": "business",
            "score": 10,
        },
    ]

    database.save_articles(articles)

    result = database.get_articles(
        category="technology"
    )

    assert len(result) == 1
    assert result[0]["title"] == "Technology Article"

def test_get_articles_filters_by_source(test_database):

    articles = [
        {
            "title": "BBC Article",
            "url": "https://example.com/bbc",
            "published": None,
            "summary": "BBC summary",
            "source": "BBC",
            "category": "technology",
            "score": 20,
        },
        {
            "title": "CNN Article",
            "url": "https://example.com/cnn",
            "published": None,
            "summary": "CNN summary",
            "source": "CNN",
            "category": "technology",
            "score": 10,
        },
    ]

    database.save_articles(articles)

    result = database.get_articles(
        source="BBC"
    )

    assert len(result) == 1
    assert result[0]["title"] == "BBC Article"

def test_get_article(test_database):

    articles = [
        {
            "title": "Test Article",
            "url": "https://example.com/test",
            "published": None,
            "summary": "Test summary",
            "source": "Test Source",
            "category": "technology",
            "score": 10,
        }
    ]

    database.save_articles(articles)

    saved_articles = database.get_top_articles()

    article_id = saved_articles[0]["id"]

    result = database.get_article(article_id)

    assert result is not None
    assert result["id"] == article_id
    assert result["title"] == "Test Article"
    assert result["url"] == "https://example.com/test"

def test_get_article_returns_none_for_missing_article(test_database):

    result = database.get_article(999)

    assert result is None

def test_get_articles_searches_title(
    test_database,
):
    articles = [
        {
            "title": "AI Changes Healthcare",
            "url": "https://example.com/ai",
            "published": None,
            "summary": "A technology article.",
            "source": "Test Source",
            "category": "technology",
            "score": 10,
        },
        {
            "title": "Football Championship",
            "url": "https://example.com/football",
            "published": None,
            "summary": "Sports news.",
            "source": "Test Source",
            "category": "sports",
            "score": 20,
        },
    ]

    database.save_articles(articles)

    results = database.get_articles(
        search="AI"
    )

    assert len(results) == 1
    assert results[0]["title"] == "AI Changes Healthcare"

def test_get_articles_searches_summary(
    test_database,
):
    articles = [
        {
            "title": "Technology Update",
            "url": "https://example.com/technology",
            "published": None,
            "summary": "Artificial intelligence is changing software.",
            "source": "Test Source",
            "category": "technology",
            "score": 10,
        },
        {
            "title": "Sports Update",
            "url": "https://example.com/sports",
            "published": None,
            "summary": "The championship begins tomorrow.",
            "source": "Test Source",
            "category": "sports",
            "score": 20,
        },
    ]

    database.save_articles(articles)

    results = database.get_articles(
        search="artificial intelligence"
    )

    assert len(results) == 1
    assert results[0]["title"] == "Technology Update"

def test_get_articles_search_combines_with_category(
    test_database,
):
    articles = [
        {
            "title": "AI in Business",
            "url": "https://example.com/business-ai",
            "published": None,
            "summary": "AI business news.",
            "source": "Test Source",
            "category": "business",
            "score": 10,
        },
        {
            "title": "AI in Technology",
            "url": "https://example.com/technology-ai",
            "published": None,
            "summary": "AI technology news.",
            "source": "Test Source",
            "category": "technology",
            "score": 20,
        },
    ]

    database.save_articles(articles)

    results = database.get_articles(
        search="AI",
        category="technology",
    )

    assert len(results) == 1
    assert results[0]["title"] == "AI in Technology"