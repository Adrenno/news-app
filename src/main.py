from collector import fetch_feed
from sources import SOURCES


def main():
    all_articles = []

    for source in SOURCES:
        print(f"Fetching {source['name']}...")

        articles = fetch_feed(source)
        all_articles.extend(articles)

        print(f"  Found {len(articles)} articles.")

    print(f"\nTotal articles: {len(all_articles)}\n")

    for article in all_articles[:10]:
        print(f"[{article['category'].upper()}] {article['title']}")
        print(f"Source: {article['source']}")
        print(article["url"])
        print()


if __name__ == "__main__":
    main()