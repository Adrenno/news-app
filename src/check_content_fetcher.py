from content_fetcher import fetch_article_content


URL = "https://www.bbc.co.uk/news/articles/cp308wy8zk9o?at_medium=RSS&at_campaign=rss"


def main():
    content = fetch_article_content(URL)

    if content is None:
        print("Failed to extract article.")

        return

    print(content[:3000])


if __name__ == "__main__":
    main()