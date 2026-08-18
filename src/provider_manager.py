from providers import gemini
from providers import groq
from providers import openrouter


PROVIDERS = {
    "gemini": gemini.generate,
    "groq": groq.generate,
    "openrouter": openrouter.generate,
}


def generate_response(
    prompt: str,
    preferred_provider: str,
    unavailable_providers: set[str] | None = None,
) -> str:
    """
    Try the preferred provider first, then fall back
    to the other available providers.

    Providers that fail are added to unavailable_providers
    so they are not retried during the same digest run.

    Raises RuntimeError if all providers fail.
    """

    if preferred_provider not in PROVIDERS:
        raise ValueError(
            f"Unknown provider: {preferred_provider}"
        )

    if unavailable_providers is None:
        unavailable_providers = set()

    provider_order = [
        preferred_provider,
        *[
            provider
            for provider in PROVIDERS
            if provider != preferred_provider
        ],
    ]

    for provider in provider_order:

        if provider in unavailable_providers:
            print(
                f"Skipping unavailable provider: "
                f"{provider}"
            )
            continue

        generate = PROVIDERS[provider]

        print(
            f"Trying provider: {provider}"
        )

        try:
            response = generate(prompt)

            print(
                f"Provider succeeded: {provider}"
            )

            return response

        except Exception as error:
            print(
                f"Provider failed: {provider}"
            )
            print(f"Reason: {error}")

            unavailable_providers.add(provider)

    print(
        "\nAll AI providers are currently unavailable."
    )

    print(
        "The article could not be summarized."
    )

    raise RuntimeError(
        "All AI providers failed."
    )