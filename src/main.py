from collector import fetch_feed
from processor import normalize_article, deduplicate_articles
from sources import SOURCES
from ranking import rank_articles
from database import (
    initialize_database,
    save_articles,
)

initialize_database()

def main():
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

    print("\nTop articles:\n")

    for article in ranked_articles[:10]:
    
        score = article["score"]
    
        print(
            f"[{score['total']:.0f}] "
            f"[{article['category'].upper()}] "
            f"{article['title']}"
        )
    
        print(
            f"  Recency:  {score['recency']}"
            f" | Category: {score['category']}"
            f" | Keywords: {score['keywords']}"
            f" | Source: {score['source']}"
        )
    
        print(f"  Source: {article['source']}")
        print(f"  {article['url']}")
        print()


if __name__ == "__main__":
    main()