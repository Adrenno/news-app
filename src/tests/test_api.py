from fastapi.testclient import TestClient
from unittest.mock import patch

import api
import database


client = TestClient(api.app)

import pytest


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    database.initialize_database()

    return db_path


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "News App API is running."
    }


def test_get_all_digests(test_database):
    response = client.get("/api/digests")

    assert response.status_code == 200

    data = response.json()

    assert "digests" in data
    assert isinstance(data["digests"], list)

    assert "limit" in data
    assert "offset" in data

    assert data["limit"] == 20
    assert data["offset"] == 0


def test_get_all_digests_with_pagination(test_database):
    response = client.get(
        "/api/digests?limit=5&offset=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["limit"] == 5
    assert data["offset"] == 10
    assert isinstance(data["digests"], list)


def test_get_all_digests_rejects_invalid_limit(test_database):
    response = client.get(
        "/api/digests?limit=0"
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "limit must be at least 1"
    }


def test_get_all_digests_rejects_negative_offset(test_database):
    response = client.get(
        "/api/digests?offset=-1"
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "offset cannot be negative"
    }


def test_get_latest_digest(test_database):
    response = client.get("/api/digests/latest")

    assert response.status_code == 200

    data = response.json()

    assert "digest" in data


def test_get_nonexistent_digest(test_database):
    response = client.get(
        "/api/digests/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Digest not found."
    }

def create_test_digest(title, url, score):
    article = {
        "title": title,
        "url": url,
        "published": None,
        "summary": f"Summary for {title}",
        "source": "Test Source",
        "category": "technology",
        "score": score,
    }

    database.save_articles([article])

    articles = database.get_top_articles(limit=1)

    return database.create_digest_record(
        articles
    )


def create_test_article(title, url, score):
    article = {
        "title": title,
        "url": url,
        "published": None,
        "summary": f"Summary for {title}",
        "source": "Test Source",
        "category": "technology",
        "score": score,
    }

    database.save_articles([article])

    articles = database.get_top_articles(limit=1)

    return articles[0]

def test_get_digest(test_database):
    digest_id = create_test_digest(
        "Test Article",
        "https://example.com/test",
        100,
    )

    response = client.get(
        f"/api/digests/{digest_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["digest"]["id"] == digest_id
    assert data["digest"]["articles"][0]["title"] == "Test Article"
    assert data["digest"]["articles"][0]["url"] == (
        "https://example.com/test"
    )

def test_get_latest_digest_returns_latest(
    test_database,
):
    first_id = create_test_digest(
        "First Article",
        "https://example.com/first",
        10,
    )

    second_id = create_test_digest(
        "Second Article",
        "https://example.com/second",
        20,
    )

    response = client.get(
        "/api/digests/latest"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["digest"]["id"] == second_id
    assert data["digest"]["id"] != first_id

def test_get_all_digests_pagination(
    test_database,
):
    create_test_digest(
        "First Article",
        "https://example.com/first",
        10,
    )

    create_test_digest(
        "Second Article",
        "https://example.com/second",
        20,
    )

    create_test_digest(
        "Third Article",
        "https://example.com/third",
        30,
    )

    response = client.get(
        "/api/digests?limit=1&offset=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["limit"] == 1
    assert data["offset"] == 1
    assert len(data["digests"]) == 1

def test_get_digest_invalid_id():
    response = client.get(
        "/api/digests/not-a-number"
    )

    assert response.status_code == 422

def test_get_digest_returns_articles(
    test_database,
):
    digest_id = create_test_digest(
        "Test Article",
        "https://example.com/test",
        50,
    )

    response = client.get(
        f"/api/digests/{digest_id}"
    )

    assert response.status_code == 200

    data = response.json()

    digest = data["digest"]

    assert digest["id"] == digest_id
    assert len(digest["articles"]) == 1
    assert digest["articles"][0]["title"] == "Test Article"

def test_get_all_articles(test_database):
    response = client.get(
        "/api/articles"
    )

    assert response.status_code == 200

    data = response.json()

    assert "articles" in data
    assert isinstance(data["articles"], list)
    assert data["limit"] == 20
    assert data["offset"] == 0

def test_get_articles_returns_articles(
    test_database,
):
    database.save_articles([
        {
            "title": "Test Article",
            "url": "https://example.com/test",
            "published": None,
            "summary": "Test summary",
            "source": "BBC",
            "category": "technology",
            "score": 50,
        }
    ])

    response = client.get(
        "/api/articles"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["articles"]) == 1
    assert data["articles"][0]["title"] == (
        "Test Article"
    )

def test_get_articles_with_category_filter(
    test_database,
):
    database.save_articles([
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
    ])

    response = client.get(
        "/api/articles?category=technology"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["articles"]) == 1
    assert data["articles"][0]["category"] == (
        "technology"
    )

def test_get_articles_rejects_invalid_limit(
    test_database,
):
    response = client.get(
        "/api/articles?limit=0"
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "limit must be at least 1"
    }


def test_get_articles_rejects_negative_offset(
    test_database,
):
    response = client.get(
        "/api/articles?offset=-1"
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "offset cannot be negative"
    }

def test_get_why_it_matters():
    article = create_test_article(
        "Important Article",
        "https://example.com/important",
        10,
    )

    with patch(
        "api.get_article",
        return_value=article,
    ), patch(
        "api.summarize_article",
        return_value={
            "summary": "Article summary",
            "why_it_matters": "This matters because it affects the industry.",
        },
    ):
        response = client.post(
            f"/api/articles/{article['id']}/why-it-matters"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["article_id"] == article["id"]

    assert (
        data["why_it_matters"]
        == "This matters because it affects the industry."
    )

def test_get_why_it_matters_article_not_found():
    with patch(
        "api.get_article",
        return_value=None,
    ):
        response = client.post(
            "/api/articles/999999/why-it-matters"
        )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Article not found."
    }

def test_get_why_it_matters_does_not_save_article():
    article = create_test_article(
        "Temporary Context Article",
        "https://example.com/temporary",
        10,
    )

    with patch(
        "api.get_article",
        return_value=article,
    ), patch(
        "api.summarize_article",
        return_value={
            "summary": "Article summary",
            "why_it_matters": "Temporary explanation.",
        },
    ):
        response = client.post(
            f"/api/articles/{article['id']}/why-it-matters"
        )

    assert response.status_code == 200

    assert response.json()["why_it_matters"] == (
        "Temporary explanation."
    )

