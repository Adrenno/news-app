import requests
import trafilatura


TIMEOUT = 15

MAX_CONTENT_LENGTH = 20000

def fetch_article_content(url: str) -> str | None:
    """
    Fetch and extract the main text from an article URL.

    Returns None if the article cannot be fetched or parsed.
    """

    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/151.0 Safari/537.36"
                )
            },
        )

        response.raise_for_status()

        text = trafilatura.extract(
            response.text
        )

        if text is None:
            return None

        return text[:MAX_CONTENT_LENGTH]

    except requests.RequestException as error:
        print(
            f"  Failed to fetch article: {error}"
        )

        return None