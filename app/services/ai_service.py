"""AI service interface for JARVIS.

The provider integration will be added after API credentials are configured.
"""

from app.core.config import settings


class AIServiceNotConfiguredError(Exception):
    """Raised when the AI provider is not ready to handle requests."""


async def generate_reply(message: str) -> str:
    """Generate an assistant reply.

    This initial implementation deliberately does not return a fake response.
    """
    if not settings.openai_api_key:
        raise AIServiceNotConfiguredError(
            "AI provider is not configured. Add an API key before using chat."
        )

    raise NotImplementedError(
        "The AI provider integration has not been implemented yet."
    )
