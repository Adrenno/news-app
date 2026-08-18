from html import unescape
import re

MINIMUM_DIGEST_SCORE = 12

CATEGORY_ORDER = [
    "taiwan",
    "world",
    "business",
    "programming",
    "technology",
]


def clean_summary(summary: str) -> str:
    """Clean HTML and whitespace from an article summary."""

    summary = unescape(summary)

    # Remove HTML tags.
    summary = re.sub(r"<[^>]+>", "", summary)

    # Normalize whitespace.
    summary = re.sub(r"\s+", " ", summary)

    return summary.strip()


def group_by_category(articles: list[dict]) -> dict:
    """Group articles according to their category."""

    grouped = {}

    for article in articles:
        category = article["category"]

        if category not in grouped:
            grouped[category] = []

        grouped[category].append(article)

    return grouped


def filter_important_articles(
    articles: list[dict],
) -> list[dict]:
    """Keep only articles worth including in a digest."""

    return [
        article
        for article in articles
        if article["score"] >= MINIMUM_DIGEST_SCORE
    ]


def generate_digest(
    articles: list[dict],
    articles_per_category: int = 3,
) -> dict:
    """Generate structured digest data for the client."""

    grouped = group_by_category(articles)

    digest_articles = []

    for category in CATEGORY_ORDER:

        category_articles = grouped.get(category, [])

        for article in category_articles[
            :articles_per_category
        ]:
            digest_articles.append({
                "title": article["title"],
                "summary": clean_summary(
                    article.get("summary", "")
                ) or "No summary available.",
                "why_it_matters": clean_summary(
                    article.get("why_it_matters", "")
                ),
                "url": article["url"],
                "source": article["source"],
                "category": article["category"],
                "published": article.get("published"),
                "score": article["score"],
            })

    return {
        "articles": digest_articles,
    }