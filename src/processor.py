import re
from html import unescape


def clean_text(text: str) -> str:
    """Remove HTML and normalize whitespace."""

    text = unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_title(title: str) -> str:
    """Create a simplified version of a title for comparison."""

    title = clean_text(title).lower()
    title = re.sub(r"[^a-z0-9\s]", "", title)
    title = re.sub(r"\s+", " ", title)

    return title.strip()


def normalize_article(article: dict) -> dict:
    """Clean and normalize an article."""

    return {
        **article,
        "title": clean_text(article["title"]),
        "summary": clean_text(article["summary"]),
        "normalized_title": normalize_title(article["title"]),
    }


def deduplicate_articles(articles: list[dict]) -> list[dict]:
    """Remove articles with identical normalized titles."""

    seen_titles = set()
    unique_articles = []

    for article in articles:
        title = article["normalized_title"]

        if title in seen_titles:
            continue

        seen_titles.add(title)
        unique_articles.append(article)

    return unique_articles

def create_article(
    title: str,
    url: str,
    published: str,
    summary: str,
    source: str,
    category: str,
) -> dict:
    """Create an article with the standard structure."""

    return {
        "title": clean_text(title),
        "url": url.strip(),
        "published": published,
        "summary": clean_text(summary),
        "source": source,
        "category": category,
        "score": 0.0,
    }