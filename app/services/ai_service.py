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


def _send_ollama_request(message: str) -> str:
    """Send a chat request to the local Ollama HTTP API."""

    url = f"{settings.ollama_base_url.rstrip('/')}/api/chat"
    payload = {
        "model": settings.ollama_model,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are JARVIS, the user's personal AI assistant. "
                    "You are not a fictional movie character. Do not invent "
                    "personal details, devices, permissions, or actions. "
                    "Be helpful, accurate, and concise. Reply in the language "
                    "used by the user."
                ),
            },
            {"role": "user", "content": message},
        ],
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


async def generate_reply(message: str) -> str:
    """Generate a reply using the configured local Ollama model."""

    if settings.ai_provider.lower() != "ollama":
        raise AIServiceNotConfiguredError(
            f"Unsupported AI provider: {settings.ai_provider}"
        )

    return await asyncio.to_thread(_send_ollama_request, message)
