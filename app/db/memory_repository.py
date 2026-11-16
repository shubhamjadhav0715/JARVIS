"""Database operations for JARVIS personal memories."""

import sqlite3

from app.db.database import get_connection


def save_memory(category: str, memory_key: str, memory_value: str) -> int:
    """Create or update a memory using its unique key."""

    clean_category = category.strip()
    clean_key = memory_key.strip()
    clean_value = memory_value.strip()

    if not clean_category or not clean_key or not clean_value:
        raise ValueError("Memory category, key, and value cannot be empty.")

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO memories (category, memory_key, memory_value)
            VALUES (?, ?, ?)
            ON CONFLICT(memory_key) DO UPDATE SET
                category = excluded.category,
                memory_value = excluded.memory_value,
                updated_at = CURRENT_TIMESTAMP
            """,
            (clean_category, clean_key, clean_value),
        )

        connection.commit()

        row = connection.execute(
            "SELECT id FROM memories WHERE memory_key = ?",
            (clean_key,),
        ).fetchone()

        return int(row["id"])

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_all_memories() -> list[dict]:
    """Return all saved personal memories."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT id, category, memory_key, memory_value,
                   created_at, updated_at
            FROM memories
            ORDER BY category ASC, memory_key ASC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_memory(memory_key: str) -> dict | None:
    """Return one memory by its unique key."""

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT id, category, memory_key, memory_value,
                   created_at, updated_at
            FROM memories
            WHERE memory_key = ?
            """,
            (memory_key.strip(),),
        ).fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def delete_memory(memory_key: str) -> bool:
    """Delete one memory by its unique key."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM memories WHERE memory_key = ?",
            (memory_key.strip(),),
        )
        connection.commit()
        return cursor.rowcount > 0

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()
