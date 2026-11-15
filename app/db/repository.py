
import sqlite3

from app.db.database import get_connection


def create_conversation(title: str) -> int:
    """Create a conversation and return its ID."""

    if not title.strip():
        raise ValueError("Conversation title cannot be empty.")

    connection = get_connection()

    try:
        cursor = connection.execute(
            "INSERT INTO conversations (title) VALUES (?)",
            (title.strip(),)
        )

        connection.commit()
        return int(cursor.lastrowid)

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def add_message(
    conversation_id: int,
    role: str,
    content: str
) -> int:
    """Save a message and return its ID."""

    if role not in ("user", "assistant", "system"):
        raise ValueError("Invalid message role.")

    if not content.strip():
        raise ValueError("Message content cannot be empty.")

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO messages
                (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content.strip())
        )

        connection.execute(
            """
            UPDATE conversations
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (conversation_id,)
        )

        connection.commit()
        return int(cursor.lastrowid)

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_messages(conversation_id: int) -> list[dict]:
    """Retrieve messages from a conversation."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT id, conversation_id, role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,)
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_conversation(conversation_id: int) -> dict | None:
    """Retrieve a conversation by its ID."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT id, title, created_at, updated_at
            FROM conversations
            WHERE id = ?
            """,
            (conversation_id,)
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def get_all_conversations() -> list[dict]:
    """Retrieve all conversations."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT id, title, created_at, updated_at
            FROM conversations
            ORDER BY updated_at DESC, id DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()

def update_conversation_title(
    conversation_id: int,
    new_title: str
) -> bool:
    """Update a conversation title."""

    if not new_title.strip():
        raise ValueError("Conversation title cannot be empty.")

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE conversations
            SET title = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (new_title.strip(), conversation_id)
        )

        connection.commit()

        return cursor.rowcount > 0

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()

def delete_conversation(conversation_id: int) -> bool:
    """Delete a conversation and its messages."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM conversations
            WHERE id = ?
            """,
            (conversation_id,)
        )

        connection.commit()

        return cursor.rowcount > 0

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()