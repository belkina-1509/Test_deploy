import logging
import os
import re
import sqlite3
from typing import Iterable, Optional, Tuple

DB_PATH = os.getenv("APP_DATABASE", "test.db")
LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "INFO").upper()

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_.-]{3,32}$")
DEFAULT_LIST_LIMIT = 100


def configure_logging() -> None:
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def create_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE
        )
        """
    )
    conn.commit()


def validate_username(raw: str) -> str:
    username = raw.strip()
    if not USERNAME_RE.match(username):
        raise ValueError(
            "Username must be 3-32 chars: letters, digits, underscore, dot, dash."
        )
    return username


def parse_int(raw: str) -> int:
    value = int(raw.strip())
    if value <= 0:
        raise ValueError("ID must be a positive integer.")
    return value


def add_user(conn: sqlite3.Connection, username: str) -> int:
    cursor = conn.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    return int(cursor.lastrowid)


def get_user_by_username(
    conn: sqlite3.Connection, username: str
) -> Iterable[sqlite3.Row]:
    cursor = conn.execute("SELECT id, username FROM users WHERE username = ?", (username,))
    return cursor.fetchall()


def delete_user_by_id(conn: sqlite3.Connection, user_id: int) -> int:
    cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return cursor.rowcount


def list_users(
    conn: sqlite3.Connection, limit: int = DEFAULT_LIST_LIMIT, offset: int = 0
) -> Iterable[sqlite3.Row]:
    cursor = conn.execute(
        "SELECT id, username FROM users ORDER BY id LIMIT ? OFFSET ?",
        (limit, offset),
    )
    return cursor.fetchall()


def prompt(message: str) -> str:
    return input(message).strip()


def main() -> int:
    configure_logging()
    logging.info("Starting user database CLI")

    try:
        with create_connection() as conn:
            init_db(conn)
    except sqlite3.Error as exc:
        logging.error("Failed to initialize DB: %s", exc)
        return 1

    while True:
        print("\n1. Search user")
        print("2. Add user")
        print("3. Delete user")
        print("4. Show all users")
        print("5. Exit")

        choice = prompt("Select: ")

        try:
            with create_connection() as conn:
                if choice == "1":
                    username = validate_username(prompt("Enter username to search: "))
                    results = get_user_by_username(conn, username)
                    if results:
                        for row in results:
                            print(f"{row['id']}: {row['username']}")
                    else:
                        print("No users found.")

                elif choice == "2":
                    username = validate_username(prompt("Enter username: "))
                    user_id = add_user(conn, username)
                    print(f"User created with id {user_id}.")

                elif choice == "3":
                    user_id = parse_int(prompt("Enter user ID to delete: "))
                    deleted = delete_user_by_id(conn, user_id)
                    print("Deleted." if deleted else "User not found.")

                elif choice == "4":
                    users = list_users(conn)
                    if not users:
                        print("No users in database.")
                    for row in users:
                        print(f"{row['id']}: {row['username']}")

                elif choice == "5":
                    return 0

                else:
                    print("Invalid choice")

        except ValueError as exc:
            print(f"Input error: {exc}")
        except sqlite3.IntegrityError:
            print("Username already exists.")
        except sqlite3.Error as exc:
            logging.error("Database error: %s", exc)


if __name__ == "__main__":
    raise SystemExit(main())