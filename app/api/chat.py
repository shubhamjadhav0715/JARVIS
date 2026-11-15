"""Chat API routes for JARVIS."""

from fastapi import APIRouter, HTTPException, status

from app.db.repository import add_message, get_conversation
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import (
    AIServiceNotConfiguredError,
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
    """Send a message to JARVIS and receive an AI reply."""

    conversation = get_conversation(request.conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    try:
        assistant_message = await generate_reply(request.message)

    except AIServiceNotConfiguredError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error

    except NotImplementedError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI provider integration is not implemented yet.",
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
