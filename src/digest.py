from html import unescape
import re

MINIMUM_DIGEST_SCORE = 12

# ------------------------------------------------------------
# CATEGORY DISPLAY
# ------------------------------------------------------------
#
# Internal category names are simple strings:
#
#     taiwan
#     world
#     business
#     programming
#     technology
#
# The digest can display nicer labels/icons.
# ------------------------------------------------------------

CATEGORY_DISPLAY = {
    "taiwan": "🇹🇼 TAIWAN",
    "world": "🌎 WORLD",
    "business": "💰 BUSINESS",
    "programming": "💻 PROGRAMMING",
    "technology": "⚙️ TECHNOLOGY",
}


def clean_summary(summary: str) -> str:
    """Clean HTML and whitespace from an article summary."""

    summary = unescape(summary)

    # Remove HTML tags.
    summary = re.sub(r"<[^>]+>", "", summary)

    # Normalize whitespace.
    summary = re.sub(r"\s+", " ", summary)

    return summary.strip()

def format_article(article: dict) -> str:
    """Format one article for the digest."""

    title = article["title"]
    summary = clean_summary(article["summary"])
    url = article["url"]

    if not summary:
        summary = "No summary available."

    return (
        f"### {title}\n\n"
        f"{summary}\n\n"
        f"**Read original →** {url}\n"
    )

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
        if article["score"]["total"] >= MINIMUM_DIGEST_SCORE
    ]

def generate_digest(
    articles: list[dict],
    articles_per_category: int = 3,
) -> str:
    """Generate a readable news digest."""

    grouped = group_by_category(articles)

    lines = []

    lines.append("=" * 50)
    lines.append("YOUR NEWS DIGEST")
    lines.append("=" * 50)
    lines.append("")

    # Display categories in this order.
    category_order = [
        "taiwan",
        "world",
        "business",
        "programming",
        "technology",
    ]

    for category in category_order:

        category_articles = grouped.get(category, [])

        if not category_articles:
            continue

        lines.append(
            CATEGORY_DISPLAY.get(
                category,
                category.upper(),
            )
        )

        lines.append("")

        for article in category_articles[
            :articles_per_category
        ]:
            lines.append(
                format_article(article)
            )
            lines.append("-" * 50)
            lines.append("")

    return "\n".join(lines)