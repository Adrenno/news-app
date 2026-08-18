from summarizer import summarize_article


TEST_ARTICLE = {
    "title": "Example technology article",
    "category": "technology",
    "summary": (
        "A technology company announced a new processor "
        "designed to improve performance while using less power."
    ),
}


def main():
    result = summarize_article(
        TEST_ARTICLE,
        provider="openrouter", #change between gemini, groq, openrouter for manual testing
    )

    print("SUMMARY:")
    print(result["summary"])

    print("\nWHY IT MATTERS:")
    print(result["why_it_matters"])


if __name__ == "__main__":
    main()