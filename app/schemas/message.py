
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MessageCreate(BaseModel):
    """Validate incoming user messages."""

    model_config = ConfigDict(str_strip_whitespace=True)

    content: str = Field(
        min_length=1,
        max_length=10000,
        description="Message content"
    )


class MessageRead(BaseModel):
    """Structure returned message data."""

    id: int
    conversation_id: int
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: str
