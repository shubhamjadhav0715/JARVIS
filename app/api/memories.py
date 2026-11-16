"""API routes for managing JARVIS personal memories."""

from fastapi import APIRouter, HTTPException, status

from app.db.memory_repository import (
    delete_memory,
    get_all_memories,
    get_memory,
    save_memory,
)
from app.schemas.memory import MemoryCreate, MemoryRead


router = APIRouter(
    prefix="/memories",
    tags=["Memories"],
)


@router.get("", response_model=list[MemoryRead])
def list_memories():
    """Return all saved memories."""

    try:
        return get_all_memories()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve memories.",
        ) from error


@router.post(
    "",
    response_model=MemoryRead,
    status_code=status.HTTP_200_OK,
)
def create_or_update_memory(request: MemoryCreate):
    """Save a memory or update it when its key already exists."""

    try:
        save_memory(
            request.category,
            request.memory_key,
            request.memory_value,
        )
        memory = get_memory(request.memory_key)

        if memory is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Memory could not be retrieved after saving.",
            )

        return memory

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save memory.",
        ) from error


@router.delete("/{memory_key}")
def remove_memory(memory_key: str):
    """Delete one saved memory by its key."""

    try:
        deleted = delete_memory(memory_key)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Memory not found.",
            )

        return {
            "message": "Memory deleted successfully.",
            "memory_key": memory_key,
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete memory.",
        ) from error
