import argparse
from config import SUMMARY_PROVIDER
from content_fetcher import fetch_article_content
from summarizer import summarize_article


def main():
    parser = argparse.ArgumentParser(
        description="Test article summarization."
    )

    parser.add_argument(
        "url",
        help="URL of the article to summarize",
    )

    parser.add_argument(
        "--provider",
        choices=[
            "gemini",
            "groq",
            "openrouter",
        ],
        help=(
            "AI provider to use. "
            "Defaults to SUMMARY_PROVIDER in .env."
        ),
    )

    parser.add_argument(
        "--title",
        required=True,
        help="Title of the article.",
    )

    args = parser.parse_args()

    print("\nFetching article...")

    content = fetch_article_content(args.url)

    if content is None:
        print("Failed to fetch article.")
        return

    print(
        f"Article content: {len(content)} characters"
    )

    article = {
        "title": args.title,
        "category": "test",
        "url": args.url,
        "summary": "",
    }

    provider = args.provider or SUMMARY_PROVIDER

    print(f"Using provider: {provider}")

    print("\nGenerating summary...\n")

    result = summarize_article(
        article,
        content=content,
        provider=provider,
    )

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(result["summary"])

    print("\n" + "=" * 60)
    print("WHY IT MATTERS")
    print("=" * 60)
    print(result["why_it_matters"])


if __name__ == "__main__":
    main()

#for testing:
#python src/test_article.py "https://www.bbc.com/news/articles/cp308wy8zk9o?at_medium=RSS&at_campaign=rss" --title "I paid £400 for a Prada bag on Vinted - only to find it was fake"