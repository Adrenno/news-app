import feedparser


def fetch_feed(source: dict) -> list[dict]:
    try:
        feed = feedparser.parse(source["url"])

        articles = []

        for entry in feed.entries:
            articles.append({
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", ""),
                "source": source["name"],
                "category": source["category"],
            })

        return articles

    except Exception as error:
        print(f"Failed to fetch {source['name']}: {error}")
        return []