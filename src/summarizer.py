from content_fetcher import fetch_article_content
from config import SUMMARY_PROVIDER
from provider_manager import generate_response


DEFAULT_PROVIDER = SUMMARY_PROVIDER


def summarize_article(
    article: dict,
    content: str | None = None,
    provider: str = DEFAULT_PROVIDER,
    unavailable_providers: set[str] | None = None,
) -> dict:
    """
    Generate a summary for an article.
    """

    if content is None:
        content = fetch_article_content(
            article["url"]
        )

    if content is None:
        content = article["summary"]

    prompt = f"""
You are a news summarizer.

Your job is to help the reader understand important
news without doing all the reading for them.

Article title:
{article["title"]}

Category:
{article["category"]}

Article content:
{content}

Write:

1. A concise summary in 2–3 short paragraphs.
2. A short explanation of why this matters.

Rules:

- Use simple, natural English.
- Prefer common words over unnecessarily advanced vocabulary.
- Keep important names, numbers, dates, and technical terms.
- Briefly explain technical terms when necessary.
- Do not add information that is not supported by the article.
- Do not repeat the title.
- "Why it matters" should explain significance rather than
  simply repeat what happened.
- Keep the total response reasonably short.

Return exactly this format:

SUMMARY:
<summary>

WHY_IT_MATTERS:
<why it matters>
"""

    response = generate_response(
        prompt,
        preferred_provider=provider,
        unavailable_providers=unavailable_providers,
    )

    return parse_response(response)

def parse_response(response: str) -> dict:
    """Extract the summary sections from the model response."""

    summary_marker = "SUMMARY:"
    why_marker = "WHY_IT_MATTERS:"

    if summary_marker not in response:
        return {
            "summary": response.strip(),
            "why_it_matters": "",
        }

    summary_part = response.split(
        summary_marker,
        1,
    )[1]

    if why_marker not in summary_part:
        return {
            "summary": summary_part.strip(),
            "why_it_matters": "",
        }

    summary, why_it_matters = summary_part.split(
        why_marker,
        1,
    )

    return {
        "summary": summary.strip(),
        "why_it_matters": why_it_matters.strip(),
    }