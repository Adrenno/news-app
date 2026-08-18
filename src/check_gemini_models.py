from google import genai

from config import GEMINI_API_KEY


def main():
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    print("Available Gemini models:\n")

    for model in client.models.list():
        if "generateContent" in model.supported_actions:
            print(model.name)


if __name__ == "__main__":
    main()