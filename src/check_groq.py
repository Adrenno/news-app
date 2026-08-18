from groq import Groq

from config import GROQ_API_KEY


def main():
    client = Groq(
        api_key=GROQ_API_KEY
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": (
                    "Explain what a CPU is "
                    "in one sentence."
                ),
            }
        ],
    )

    print(
        response.choices[0].message.content
    )


if __name__ == "__main__":
    main()