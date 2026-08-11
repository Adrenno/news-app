from datetime import datetime, timezone


# ============================================================
# RANKING CONFIGURATION
# ============================================================
#
# These values control how much each criterion contributes
# to an article's final ranking score.
#
# We will tune these values as we use the application.
# ============================================================


# ------------------------------------------------------------
# CATEGORY WEIGHTS
# ------------------------------------------------------------
#
# Higher number = category is more important to us.
#
# Example:
#   programming = 10
#   technology  = 8
#
# means programming articles receive a larger boost than
# technology articles.
# ------------------------------------------------------------

CATEGORY_WEIGHTS = {
    "taiwan": 10,
    "programming": 10,
    "technology": 8,
    "business": 7,
    "world": 6,
}


# ------------------------------------------------------------
# KEYWORD WEIGHTS
# ------------------------------------------------------------
#
# Articles whose titles contain these words receive an
# additional boost.
#
# This is intentionally simple for now. Later we can make
# this much more sophisticated.
# ------------------------------------------------------------

KEYWORD_WEIGHTS = {
    "python": 5,
    "ai": 5,
    "artificial intelligence": 5,
    "semiconductor": 5,
    "chip": 4,
    "software": 3,
    "programming": 4,
}


# ------------------------------------------------------------
# SOURCE WEIGHTS
# ------------------------------------------------------------
#
# Some sources may eventually be considered more useful
# than others.
#
# We haven't decided our final sources yet, so these are
# intentionally modest values for now.
# ------------------------------------------------------------

SOURCE_WEIGHTS = {
    "BBC World": 3,
    "BBC Technology": 3,
    "BBC Business": 3,
}


# ------------------------------------------------------------
# RECENCY
# ------------------------------------------------------------
#
# Newer articles should generally appear above older ones.
#
# For now, we use a simple time-based score:
#
#   < 6 hours   -> 10 points
#   < 12 hours  -> 8 points
#   < 24 hours  -> 5 points
#   < 48 hours  -> 2 points
#   older       -> 0 points
#
# This is deliberately simple and easy to tune.
# ------------------------------------------------------------

def recency_score(published: str) -> float:
    if not published:
        return 0

    try:
        # feedparser normally gives us RFC 822-style dates.
        published_time = datetime.strptime(
            published,
            "%a, %d %b %Y %H:%M:%S %Z"
        ).replace(tzinfo=timezone.utc)

    except ValueError:
        return 0

    age_hours = (
        datetime.now(timezone.utc) - published_time
    ).total_seconds() / 3600

    if age_hours < 6:
        return 10
    elif age_hours < 12:
        return 8
    elif age_hours < 24:
        return 5
    elif age_hours < 48:
        return 2

    return 0


# ------------------------------------------------------------
# CATEGORY SCORE
# ------------------------------------------------------------

def category_score(category: str) -> int:
    return CATEGORY_WEIGHTS.get(category, 0)


# ------------------------------------------------------------
# KEYWORD SCORE
# ------------------------------------------------------------
#
# We look at the article title for now.
#
# Later we can consider:
#   - title
#   - summary
#   - named entities
#   - article content
#   - user's reading history
# ------------------------------------------------------------

def keyword_score(title: str) -> int:
    title = title.lower()

    score = 0

    for keyword, weight in KEYWORD_WEIGHTS.items():
        if keyword in title:
            score += weight

    return score


# ------------------------------------------------------------
# SOURCE SCORE
# ------------------------------------------------------------

def source_score(source: str) -> int:
    return SOURCE_WEIGHTS.get(source, 0)


# ------------------------------------------------------------
# FINAL ARTICLE SCORE
# ------------------------------------------------------------
#
# This is the function we'll eventually spend a LOT of time
# tuning.
#
# Each component represents a different reason why an article
# might deserve our attention.
# ------------------------------------------------------------

def calculate_score(article: dict) -> dict:

    recency = recency_score(article["published"])
    category = category_score(article["category"])
    keywords = keyword_score(article["title"])
    source = source_score(article["source"])

    total = (
        recency
        + category
        + keywords
        + source
    )

    return {
        "total": total,
        "recency": recency,
        "category": category,
        "keywords": keywords,
        "source": source,
    }


# ------------------------------------------------------------
# RANK ARTICLES
# ------------------------------------------------------------

def rank_articles(articles: list[dict]) -> list[dict]:

    ranked_articles = []

    for article in articles:

        scores = calculate_score(article)

        ranked_articles.append({
            **article,
            "score": scores,
        })

    ranked_articles.sort(
        key=lambda article: article["score"]["total"],
        reverse=True,
    )

    return ranked_articles

