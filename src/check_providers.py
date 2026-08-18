from config import (
    GEMINI_API_KEY,
    GROQ_API_KEY,
    OPENROUTER_API_KEY,
)


def main():
    print(
        "Gemini:",
        "configured" if GEMINI_API_KEY else "missing",
    )

    print(
        "Groq:",
        "configured" if GROQ_API_KEY else "missing",
    )

    print(
        "OpenRouter:",
        "configured"
        if OPENROUTER_API_KEY
        else "missing",
    )


if __name__ == "__main__":
    main()