"""OpenAI-powered AI service for JARVIS."""

from openai import AsyncOpenAI

from app.core.config import settings


class AIServiceNotConfiguredError(Exception):
    """Raised when the AI provider is not configured."""


async def generate_reply(message: str) -> str:
    """Generate a reply using the configured OpenAI model."""

    if not settings.openai_api_key:
        raise AIServiceNotConfiguredError(
            "AI provider is not configured. Add an API key before using chat."
        )

    client = AsyncOpenAI(api_key=settings.openai_api_key)

    try:
        response = await client.responses.create(
            model=settings.openai_model,
            instructions=(
                "You are JARVIS, a helpful personal AI assistant. "
                "Be clear, accurate, and concise. Do not claim to perform "
                "actions unless they have actually been completed."
            ),
            input=message,
            max_output_tokens=300,
            store=False,
        )

        reply = response.output_text.strip()

        if not reply:
            raise RuntimeError("The AI provider returned an empty response.")

        return reply

    finally:
        await client.close()
