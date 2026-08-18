from unittest.mock import patch

import pytest

from provider_manager import generate_response


def test_preferred_provider_is_used_first():
    with patch(
        "provider_manager.PROVIDERS",
        {
            "gemini": lambda prompt: "Gemini response",
            "groq": lambda prompt: "Groq response",
            "openrouter": lambda prompt: "OpenRouter response",
        },
    ):
        result = generate_response(
            "Test prompt",
            preferred_provider="gemini",
        )

    assert result == "Gemini response"


def test_fallback_provider_is_used_when_preferred_fails():
    def failing_gemini(prompt):
        raise RuntimeError("Gemini failed")

    with patch(
        "provider_manager.PROVIDERS",
        {
            "gemini": failing_gemini,
            "groq": lambda prompt: "Groq response",
            "openrouter": lambda prompt: "OpenRouter response",
        },
    ):
        result = generate_response(
            "Test prompt",
            preferred_provider="gemini",
        )

    assert result == "Groq response"


def test_provider_order_starts_with_preferred_provider():
    calls = []

    def gemini(prompt):
        calls.append("gemini")
        raise RuntimeError("Gemini failed")

    def groq(prompt):
        calls.append("groq")
        return "Groq response"

    def openrouter(prompt):
        calls.append("openrouter")
        return "OpenRouter response"

    with patch(
        "provider_manager.PROVIDERS",
        {
            "gemini": gemini,
            "groq": groq,
            "openrouter": openrouter,
        },
    ):
        result = generate_response(
            "Test prompt",
            preferred_provider="gemini",
        )

    assert result == "Groq response"
    assert calls == ["gemini", "groq"]


def test_fallback_can_reach_openrouter():
    def failing_gemini(prompt):
        raise RuntimeError("Gemini failed")

    def failing_groq(prompt):
        raise RuntimeError("Groq failed")

    with patch(
        "provider_manager.PROVIDERS",
        {
            "gemini": failing_gemini,
            "groq": failing_groq,
            "openrouter": lambda prompt: "OpenRouter response",
        },
    ):
        result = generate_response(
            "Test prompt",
            preferred_provider="gemini",
        )

    assert result == "OpenRouter response"


def test_all_providers_failing_raises_runtime_error():
    def failing_provider(prompt):
        raise RuntimeError("Provider failed")

    with patch(
        "provider_manager.PROVIDERS",
        {
            "gemini": failing_provider,
            "groq": failing_provider,
            "openrouter": failing_provider,
        },
    ):
        with pytest.raises(
            RuntimeError,
            match="All AI providers failed",
        ):
            generate_response(
                "Test prompt",
                preferred_provider="gemini",
            )


def test_unknown_provider_raises_value_error():
    with pytest.raises(
        ValueError,
        match="Unknown provider",
    ):
        generate_response(
            "Test prompt",
            preferred_provider="does-not-exist",
        )