import argparse
from collector import fetch_feed
from processor import normalize_article, deduplicate_articles
from sources import SOURCES
from ranking import rank_articles
from database import (
    initialize_database,
    save_articles,
    create_digest_record,
    get_recent_articles,
)
from digest import (
    generate_digest,
    filter_important_articles,
)
from summarizer import summarize_article

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--test-digest",
        action="store_true",
        help="Generate a digest without using the last digest timestamp.",
    )

    args = parser.parse_args()

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

    if args.test_digest:
        print("TEST DIGEST MODE")
        print("Using all fetched articles.\n")

        articles_for_digest = ranked_articles

    else:
        articles_for_digest = get_recent_articles(
            hours=12
        )

    important_articles = filter_important_articles(
        articles_for_digest
    )

    summarized_articles = []

    unavailable_providers = set()

    for index, article in enumerate(
        important_articles,
        start=1,
    ):
        print(
            f"Summarizing article "
            f"{index}/{len(important_articles)}: "
            f"{article['title']}"
        )

        try:
            summary = summarize_article(
                article,
                unavailable_providers=unavailable_providers,
            )

        except RuntimeError as error:
            print(
                "\nWARNING: Could not summarize article."
            )
            print(error)

            continue

        summarized_articles.append({
            **article,
            "summary": summary["summary"],
            "why_it_matters": summary["why_it_matters"],
        })


    digest = generate_digest(summarized_articles)

    print("\n")
    print(digest)


    if not args.test_digest:
        create_digest_record(summarized_articles)

    else:
        print("\nTEST DIGEST MODE: digest record not saved.")


if __name__ == "__main__":
    main()