import sqlite3

from database import get_connection


def main():
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            source,
            category,
            score,
            created_at
        FROM articles
        ORDER BY created_at DESC
        LIMIT 20
    """)

    articles = cursor.fetchall()

    for article in articles:
        print(f"[{article['id']}] {article['title']}")
        print(f"  Source: {article['source']}")
        print(f"  Category: {article['category']}")
        print(f"  Score: {article['score']}")
        print(f"  Created: {article['created_at']}")
        print()


if __name__ == "__main__":
    main()