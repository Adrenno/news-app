from google import genai

from config import GEMINI_API_KEY


def main():
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Explain what a CPU is in one sentence.",
    )

    print(response.text)


if __name__ == "__main__":
    main()