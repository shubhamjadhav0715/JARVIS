"""Pydantic schemas for JARVIS personal memories."""

from pydantic import BaseModel, ConfigDict, Field


class MemoryCreate(BaseModel):
    """Validate a request to save or update a memory."""

    model_config = ConfigDict(str_strip_whitespace=True)

    category: str = Field(min_length=1, max_length=50)
    memory_key: str = Field(min_length=1, max_length=100)
    memory_value: str = Field(min_length=1, max_length=2000)


class MemoryRead(BaseModel):
    """Structure returned memory data."""

    id: int
    category: str
    memory_key: str
    memory_value: str
    created_at: str
    updated_at: str
