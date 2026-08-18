from unittest.mock import patch

import main


def make_article(
    title="Test Article",
    score=20,
):
    return {
        "title": title,
        "url": f"https://example.com/{title.lower().replace(' ', '-')}",
        "published": "Wed, 12 Aug 2026 10:00:00 GMT",
        "summary": "Test summary",
        "source": "Test Source",
        "category": "technology",
        "score": score,
    }


def test_test_digest_ignores_last_digest():
    articles = [
        make_article("Article One"),
    ]

    with (
        patch("main.initialize_database"),
        patch(
            "main.fetch_feed",
            return_value=articles,
        ),
        patch(
            "main.normalize_article",
            side_effect=lambda article: article,
        ),
        patch(
            "main.deduplicate_articles",
            return_value=articles,
        ),
        patch(
            "main.rank_articles",
            return_value=articles,
        ),
        patch("main.save_articles"),
        patch(
            "main.filter_important_articles",
            return_value=articles,
        ),
        patch(
            "main.summarize_article",
            return_value={
                "summary": "Summary",
                "why_it_matters": "Important",
            },
        ),
        patch(
            "main.generate_digest",
            return_value="DIGEST",
        ),
        patch("main.create_digest_record") as create_record,
        patch(
            "sys.argv",
            ["main.py", "--test-digest"],
        ),
    ):
        main.main()


    create_record.assert_not_called()


def test_normal_mode_uses_recent_articles():
    articles = [
        make_article("Recent Article"),
    ]

    with (
        patch("main.initialize_database"),
        patch(
            "main.fetch_feed",
            return_value=[articles[0]],
        ),
        patch(
            "main.normalize_article",
            side_effect=lambda article: article,
        ),
        patch(
            "main.deduplicate_articles",
            return_value=articles,
        ),
        patch(
            "main.rank_articles",
            return_value=articles,
        ),
        patch("main.save_articles"),
        patch(
            "main.get_recent_articles",
            return_value=articles,
        ) as get_recent_articles,
        patch(
            "main.filter_important_articles",
            return_value=articles,
        ),
        patch(
            "main.summarize_article",
            return_value={
                "summary": "Summary",
                "why_it_matters": "Important",
            },
        ),
        patch(
            "main.generate_digest",
            return_value="DIGEST",
        ),
        patch("main.create_digest_record"),
        patch(
            "sys.argv",
            ["main.py"],
        ),
    ):
        main.main()

    get_recent_articles.assert_called_once_with(
        hours=12
    )


def test_test_digest_uses_all_ranked_articles():
    articles = [
        make_article("Article One"),
        make_article("Article Two"),
    ]

    with (
        patch("main.initialize_database"),
        patch(
            "main.fetch_feed",
            return_value=articles,
        ),
        patch(
            "main.normalize_article",
            side_effect=lambda article: article,
        ),
        patch(
            "main.deduplicate_articles",
            return_value=articles,
        ),
        patch(
            "main.rank_articles",
            return_value=articles,
        ),
        patch("main.save_articles"),
        patch(
            "main.get_recent_articles",
        ) as get_recent_articles,
        patch(
            "main.filter_important_articles",
            return_value=articles,
        ) as filter_articles,
        patch(
            "main.summarize_article",
            return_value={
                "summary": "Summary",
                "why_it_matters": "Important",
            },
        ),
        patch(
            "main.generate_digest",
            return_value="DIGEST",
        ),
        patch("main.create_digest_record"),
        patch(
            "sys.argv",
            ["main.py", "--test-digest"],
        ),
    ):
        main.main()

    filter_articles.assert_called_once_with(
        articles
    )

    get_recent_articles.assert_not_called()


def test_failed_article_is_skipped():
    articles = [
        make_article("Article One"),
        make_article("Article Two"),
    ]

    def summarize(article, unavailable_providers=None):
        if article["title"] == "Article One":
            raise RuntimeError("All AI providers failed.")

        return {
            "summary": "Good summary",
            "why_it_matters": "Important",
        }

    with (
        patch("main.initialize_database"),
        patch(
            "main.fetch_feed",
            return_value=articles,
        ),
        patch(
            "main.normalize_article",
            side_effect=lambda article: article,
        ),
        patch(
            "main.deduplicate_articles",
            return_value=articles,
        ),
        patch(
            "main.rank_articles",
            return_value=articles,
        ),
        patch("main.save_articles"),
        patch(
            "main.get_recent_articles",
            return_value=articles,
        ),
        patch(
            "main.filter_important_articles",
            return_value=articles,
        ),
        patch(
            "main.summarize_article",
            side_effect=summarize,
        ),
        patch(
            "main.generate_digest",
            return_value="DIGEST",
        ) as generate_digest,
        patch("main.create_digest_record"),
        patch(
            "sys.argv",
            ["main.py"],
        ),
    ):
        main.main()

    summarized = generate_digest.call_args[0][0]

    assert len(summarized) == 1
    assert summarized[0]["title"] == "Article Two"


def test_successful_normal_digest_creates_record():
    articles = [
        make_article("Article One"),
    ]

    with (
        patch("main.initialize_database"),
        patch(
            "main.fetch_feed",
            return_value=articles,
        ),
        patch(
            "main.normalize_article",
            side_effect=lambda article: article,
        ),
        patch(
            "main.deduplicate_articles",
            return_value=articles,
        ),
        patch(
            "main.rank_articles",
            return_value=articles,
        ),
        patch("main.save_articles"),
        patch(
            "main.get_recent_articles",
            return_value=articles,
        ),
        patch(
            "main.filter_important_articles",
            return_value=articles,
        ),
        patch(
            "main.summarize_article",
            return_value={
                "summary": "Summary",
                "why_it_matters": "Important",
            },
        ),
        patch(
            "main.generate_digest",
            return_value="DIGEST",
        ),
        patch(
            "main.create_digest_record"
        ) as create_record,
        patch(
            "sys.argv",
            ["main.py"],
        ),
    ):
        main.main()

    create_record.assert_called_once()


def test_test_digest_does_not_create_record():
    articles = [
        make_article("Article One"),
    ]

    with (
        patch("main.initialize_database"),
        patch(
            "main.fetch_feed",
            return_value=articles,
        ),
        patch(
            "main.normalize_article",
            side_effect=lambda article: article,
        ),
        patch(
            "main.deduplicate_articles",
            return_value=articles,
        ),
        patch(
            "main.rank_articles",
            return_value=articles,
        ),
        patch("main.save_articles"),
        patch(
            "main.filter_important_articles",
            return_value=articles,
        ),
        patch(
            "main.summarize_article",
            return_value={
                "summary": "Summary",
                "why_it_matters": "Important",
            },
        ),
        patch(
            "main.generate_digest",
            return_value="DIGEST",
        ),
        patch(
            "main.create_digest_record"
        ) as create_record,
        patch(
            "sys.argv",
            ["main.py", "--test-digest"],
        ),
    ):
        main.main()

    create_record.assert_not_called()