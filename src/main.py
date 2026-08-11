from collector import fetch_feed
from processor import normalize_article, deduplicate_articles
from sources import SOURCES
from ranking import rank_articles
from database import (
    initialize_database,
    save_articles,
    create_digest_record,
    get_last_digest_time,
    get_articles_since,
)
from digest import (
    generate_digest,
    filter_important_articles,
)

def main():
    initialize_database()
    all_articles = []

    for source in SOURCES:
        print(f"Fetching {source['name']}...")

        articles = fetch_feed(source)

        print(f"  Found {len(articles)} articles.")

        all_articles.extend(articles)

    print(f"\nRaw articles: {len(all_articles)}")

    normalized_articles = [
        normalize_article(article)
        for article in all_articles
    ]

    unique_articles = deduplicate_articles(normalized_articles)

    print(f"Unique articles: {len(unique_articles)}\n")

    ranked_articles = rank_articles(unique_articles)

    save_articles(ranked_articles)

    last_digest = get_last_digest_time()

    if last_digest is None:
        articles_for_digest = ranked_articles
    else:
        articles_for_digest = get_articles_since(
            last_digest
        )

    important_articles = filter_important_articles(
        articles_for_digest
    )

    if important_articles:
        digest = generate_digest(
            important_articles
        )

        print(digest)

        create_digest_record()

    else:
        print(
            "\nNo important news since your "
            "last digest."
        )

        create_digest_record()


if __name__ == "__main__":
    main()