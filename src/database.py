import sqlite3
from pathlib import Path


# Location of our SQLite database.
DATABASE_PATH = Path("data/news.db")


def get_connection():
    """Create a connection to the SQLite database."""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


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
            is_read INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    try:
        cursor.execute("""
            ALTER TABLE articles
            ADD COLUMN is_read INTEGER DEFAULT 0
        """)
    except sqlite3.OperationalError:
        pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS digests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS digest_articles (
            digest_id INTEGER NOT NULL,
            article_id INTEGER NOT NULL,

            PRIMARY KEY (digest_id, article_id),

            FOREIGN KEY (digest_id)
                REFERENCES digests(id)
                ON DELETE CASCADE,

            FOREIGN KEY (article_id)
                REFERENCES articles(id)
                ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        PRAGMA table_info(articles)
    """)

    article_columns = {
        row[1]
        for row in cursor.fetchall()
    }

    if "is_read" not in article_columns:
        cursor.execute("""
            ALTER TABLE articles
            ADD COLUMN is_read INTEGER NOT NULL DEFAULT 0
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
            article["score"],
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

def get_article(article_id: int):
    """Return a single article by ID."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM articles
        WHERE id = ?
    """, (article_id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)

def get_articles(
    limit=20,
    offset=0,
    category=None,
    source=None,
    search=None,
    is_read=None,
):
    """Return paginated articles with optional filters."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    query = """
        SELECT *
        FROM articles
    """

    conditions = []
    parameters = []

    if category is not None:
        conditions.append("category = ?")
        parameters.append(category)

    if source is not None:
        conditions.append("source = ?")
        parameters.append(source)

    if search:
        conditions.append(
            "(title LIKE ? OR summary LIKE ?)"
        )

        search_term = f"%{search}%"

        parameters.extend([
            search_term,
            search_term,
        ])

    if is_read is not None:
        conditions.append("is_read = ?")
        parameters.append(1 if is_read else 0)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += """
        ORDER BY score DESC, id DESC
        LIMIT ?
        OFFSET ?
    """

    parameters.extend([
        limit,
        offset,
    ])

    cursor.execute(
        query,
        parameters,
    )

    articles = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return articles

def get_recent_articles(hours: int = 12):
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

def create_digest_record(articles: list[dict]):
    """Create a digest and associate articles with it."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO digests (
            expires_at
        )
        VALUES (
            datetime('now', '+12 hours')
        )
    """)

    digest_id = cursor.lastrowid

    for article in articles:
        cursor.execute("""
            INSERT INTO digest_articles (
                digest_id,
                article_id
            )
            VALUES (?, ?)
        """, (
            digest_id,
            article["id"],
        ))

    connection.commit()
    connection.close()

    return digest_id

def get_digests(
    limit: int = 20,
    offset: int = 0,
    digest_id: int | None = None,
):
    """Return recent digests with their associated articles."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    if digest_id is not None:

        cursor.execute("""
            SELECT id, created_at, expires_at
            FROM digests
            WHERE id = ?
        """, (digest_id,))

    else:

        cursor.execute("""
            SELECT id, created_at, expires_at
            FROM digests
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            OFFSET ?
        """, (
            limit,
            offset,
        ))

    digest_rows = cursor.fetchall()

    digests = []

    for digest in digest_rows:

        cursor.execute("""
            SELECT
                a.id,
                a.title,
                a.url,
                a.published,
                a.summary,
                a.source,
                a.category,
                a.score,
                a.is_read
            FROM digest_articles da
            JOIN articles a
                ON a.id = da.article_id
            WHERE da.digest_id = ?
            ORDER BY a.score DESC
        """, (digest["id"],))

        articles = [
            dict(row)
            for row in cursor.fetchall()
        ]

        digests.append({
            "id": digest["id"],
            "created_at": digest["created_at"],
            "expires_at": digest["expires_at"],
            "articles": articles,
        })

    connection.close()

    return digests

def get_last_digest_time():
    """Return the timestamp of the most recent digest."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT created_at
        FROM digests
        ORDER BY created_at DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    return result[0]

def get_articles_since(timestamp: str):
    """Return articles discovered since a given timestamp."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM articles
        WHERE created_at > ?
        ORDER BY score DESC
    """, (timestamp,))

    articles = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return articles

def get_active_digests():
    """Return all non-expired digests with their articles."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            d.id AS digest_id,
            d.created_at,
            d.expires_at,

            a.id AS article_id,
            a.title,
            a.url,
            a.published,
            a.summary,
            a.source,
            a.category,
            a.score

        FROM digests d

        JOIN digest_articles da
            ON d.id = da.digest_id

        JOIN articles a
            ON da.article_id = a.id

        WHERE d.expires_at > CURRENT_TIMESTAMP

        ORDER BY
            d.created_at DESC,
            a.score DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    digests = {}

    for row in rows:

        digest_id = row["digest_id"]

        if digest_id not in digests:
            digests[digest_id] = {
                "id": digest_id,
                "created_at": row["created_at"],
                "expires_at": row["expires_at"],
                "articles": [],
            }

        digests[digest_id]["articles"].append({
            "id": row["article_id"],
            "title": row["title"],
            "url": row["url"],
            "published": row["published"],
            "summary": row["summary"],
            "source": row["source"],
            "category": row["category"],
            "score": row["score"],
        })

    return list(digests.values())

def set_article_read_status(
    article_id: int,
    is_read: bool,
):
    """Set whether an article has been read."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE articles
        SET is_read = ?
        WHERE id = ?
    """, (
        1 if is_read else 0,
        article_id,
    ))

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated