
from fastapi import APIRouter, HTTPException, status

from app.db.repository import (
    create_conversation,
    get_conversation,
    add_message,
    get_messages,
    get_all_conversations,
    update_conversation_title,
)

from app.schemas.conversation import (
    ConversationCreate,
    ConversationRead,
    ConversationUpdate,
)

from app.schemas.message import (
    MessageCreate,
    MessageRead,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.post(
    "",
    response_model=ConversationRead,
    status_code=status.HTTP_201_CREATED
)
def create_new_conversation(request: ConversationCreate):
    """Create a new conversation."""

    try:
        conversation_id = create_conversation(request.title)
        conversation = get_conversation(conversation_id)

        if conversation is None:
            raise HTTPException(
                status_code=500,
                detail="Conversation could not be retrieved."
            )

        return conversation

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to create conversation."
        )


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED
)
def create_new_message(
    conversation_id: int,
    request: MessageCreate
):
    """Save a user message."""

    conversation = get_conversation(conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    try:
        message_id = add_message(
            conversation_id,
            "user",
            request.content
        )

        messages = get_messages(conversation_id)

        for message in messages:
            if message["id"] == message_id:
                return message

        raise HTTPException(
            status_code=500,
            detail="Message could not be retrieved."
        )

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to save message."
        )


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageRead]
)
def retrieve_messages(conversation_id: int):
    """Retrieve all messages from a conversation."""

    conversation = get_conversation(conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    try:
        return get_messages(conversation_id)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve messages."
        )



@router.get(
    "",
    response_model=list[ConversationRead]
)
def list_conversations():
    """Retrieve all conversations."""

    try:
        return get_all_conversations()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve conversations."
        )

@router.patch(
    "/{conversation_id}",
    response_model=ConversationRead
)
def edit_conversation(
    conversation_id: int,
    request: ConversationUpdate
):
    """Update conversation title."""

    conversation = get_conversation(conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    try:
        update_conversation_title(
            conversation_id,
            request.title
        )

        return get_conversation(conversation_id)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to update conversation."
        )