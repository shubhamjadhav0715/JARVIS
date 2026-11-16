"""Local Ollama AI service for JARVIS."""

import asyncio
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.core.config import settings


class AIServiceNotConfiguredError(Exception):
    """Raised when the selected AI provider is not configured."""


class AIServiceUnavailableError(Exception):
    """Raised when the local AI provider cannot be reached."""


def _send_ollama_request(
    message: str,
    conversation_history: list[dict] | None = None,
) -> str:
    """Send the recent conversation context and new message to Ollama."""

    url = f"{settings.ollama_base_url.rstrip('/')}/api/chat"
    ollama_messages = [
        {
            "role": "system",
            "content": (
                "You are JARVIS, the user's personal AI assistant. "
                "Use the conversation history to understand follow-up questions "
                "and remember details within this conversation. You are not a "
                "fictional movie character. Do not invent personal details, "
                "devices, permissions, or actions. Be helpful, accurate, and "
                "concise. Reply in the language used by the user."
            ),
        }
    ]

    # Keep only the latest 10 saved messages to limit memory use.
    for item in (conversation_history or [])[-10:]:
        role = item.get("role")
        content = item.get("content", "")
        if role in ("user", "assistant") and content:
            ollama_messages.append({"role": role, "content": content})

    ollama_messages.append({"role": "user", "content": message})

    payload = {
        "model": settings.ollama_model,
        "stream": False,
        "messages": ollama_messages,
        "options": {"num_predict": 300},
    }

    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

    except (URLError, TimeoutError, HTTPError) as error:
        raise AIServiceUnavailableError(
            "Cannot connect to Ollama. Make sure Ollama is running."
        ) from error

    reply = result.get("message", {}).get("content", "").strip()

    if not reply:
        raise AIServiceUnavailableError(
            "Ollama returned an empty response. Please try again."
        )

    return reply


async def generate_reply(
    message: str,
    conversation_history: list[dict] | None = None,
) -> str:
    """Generate a reply using the configured local Ollama model and history."""

    if settings.ai_provider.lower() != "ollama":
        raise AIServiceNotConfiguredError(
            f"Unsupported AI provider: {settings.ai_provider}"
        )

    return await asyncio.to_thread(
        _send_ollama_request,
        message,
        conversation_history,
    )
