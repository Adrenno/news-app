from openai import OpenAI

from config import OPENROUTER_API_KEY


MODEL = "openrouter/free"


def generate(prompt: str) -> str:
    """Generate a response using OpenRouter."""

    print(
        "OpenRouter API key loaded:",
        bool(OPENROUTER_API_KEY)
    )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content