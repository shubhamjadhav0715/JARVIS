"""Chat API routes for JARVIS."""

from fastapi import APIRouter, HTTPException, status

from app.db.memory_repository import get_all_memories
from app.db.repository import add_message, get_conversation, get_messages
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import (
    AIServiceNotConfiguredError,
    AIServiceUnavailableError,
    generate_reply,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
async def send_chat_message(request: ChatRequest):
    """Send a message to JARVIS with conversation context and permanent memories."""

    conversation = get_conversation(request.conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    try:
        conversation_history = get_messages(request.conversation_id)
        permanent_memories = get_all_memories()
        assistant_message = await generate_reply(
            request.message,
            conversation_history,
            permanent_memories,
        )

    except (AIServiceNotConfiguredError, AIServiceUnavailableError) as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate an assistant reply.",
        ) from error

    try:
        add_message(
            request.conversation_id,
            "user",
            request.message,
        )
        add_message(
            request.conversation_id,
            "assistant",
            assistant_message,
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save chat messages.",
        ) from error

    return ChatResponse(
        conversation_id=request.conversation_id,
        user_message=request.message,
        assistant_message=assistant_message,
    )
