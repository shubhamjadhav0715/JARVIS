
from pydantic import BaseModel, ConfigDict, Field


class ConversationCreate(BaseModel):
    """Validate incoming conversation creation requests."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(
        min_length=1,
        max_length=120,
        description="Title of the conversation"
    )


class ConversationRead(BaseModel):
    """Structure returned conversation data."""

    id: int
    title: str
    created_at: str
    updated_at: str


class ConversationUpdate(BaseModel):
    """Validate conversation title update requests."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(
        min_length=1,
        max_length=120,
        description="New title of the conversation"
    )
