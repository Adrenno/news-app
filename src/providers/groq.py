from groq import Groq

from config import GROQ_API_KEY


MODEL = "openai/gpt-oss-20b"


def generate(prompt: str) -> str:
    """Generate a response using Groq."""

    client = Groq(
        api_key=GROQ_API_KEY
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