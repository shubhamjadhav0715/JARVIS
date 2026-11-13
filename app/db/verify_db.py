
import sqlite3

from app.db.database import DATABASE_PATH


def verify_database():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )

        tables = cursor.fetchall()

        print("JARVIS Database Verification")
        print("----------------------------")
        print("Database exists:", DATABASE_PATH.exists())
        print("Tables found:")

        for table in tables:
            print("-", table[0])

    finally:
        connection.close()


if __name__ == "__main__":
    verify_database()
