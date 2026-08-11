import sqlite3
from pathlib import Path


# Location of our SQLite database.
DATABASE_PATH = Path("data/news.db")


def get_connection():
    """Create a connection to the SQLite database."""

    # Make sure the data directory exists.
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Create the database tables if they don't exist."""

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            published TEXT,
            summary TEXT,
            source TEXT NOT NULL,
            category TEXT NOT NULL,
            score REAL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

def save_articles(articles: list[dict]):
    """Save articles to the database."""

    connection = get_connection()
    cursor = connection.cursor()

    for article in articles:

        cursor.execute("""
            INSERT INTO articles (
                title,
                url,
                published,
                summary,
                source,
                category,
                score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(url) DO UPDATE SET
                title = excluded.title,
                published = excluded.published,
                summary = excluded.summary,
                source = excluded.source,
                category = excluded.category,
                score = excluded.score
        """, (
            article["title"],
            article["url"],
            article["published"],
            article["summary"],
            article["source"],
            article["category"],
            article["score"]["total"],
        ))

    connection.commit()
    connection.close()

def get_top_articles(limit: int = 10):
    """Return the highest-ranked articles."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM articles
        ORDER BY score DESC
        LIMIT ?
    """, (limit,))

    articles = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return articles

def get_recent_articles(hours: int = 3):
    """Return articles first seen within the last N hours."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM articles
        WHERE created_at >= datetime('now', ?)
        ORDER BY score DESC
    """, (f"-{hours} hours",))

    articles = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return articles