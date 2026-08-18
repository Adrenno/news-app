from google import genai
from google.genai import errors

from config import GEMINI_API_KEY


MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]


def generate(prompt: str) -> str:
    """Generate a response using Gemini."""

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    last_error = None

    for model in MODELS:
        try:
            print(f"[Gemini] Trying model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            print(f"[Gemini] {model} succeeded")

            return response.text

        except errors.ServerError as error:
            print(
                f"[Gemini] {model} failed: {error}"
            )

            last_error = error

    raise RuntimeError(
        "All Gemini models failed."
    ) from last_error