"""Request and response schemas for the JARVIS chat endpoint."""

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """Validate a message sent to the JARVIS chat endpoint."""

    model_config = ConfigDict(str_strip_whitespace=True)

    conversation_id: int = Field(
        gt=0,
        description="ID of the conversation to continue",
    )
    message: str = Field(
        min_length=1,
        max_length=10000,
        description="Message sent by the user",
    )


class ChatResponse(BaseModel):
    """Structure returned after JARVIS processes a chat message."""

    conversation_id: int
    user_message: str
    assistant_message: str
