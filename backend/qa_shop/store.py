"""SQLite users and revocable sessions. Each operation owns its connection."""

import hashlib
import hmac
import secrets
import sqlite3
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

PASSWORD_ROUNDS = 120_000
SESSION_SECONDS = 3600


class Store:
    """Small persistent repository; SQL parameters keep user input out of SQL syntax."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as connection:
            connection.executescript(
                "CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, "
                "salt TEXT NOT NULL, password_hash TEXT NOT NULL);"
                "CREATE TABLE IF NOT EXISTS sessions ("
                "token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL, "
                "expires REAL NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id));"
            )

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        """Return an independent connection, including for concurrent requests."""
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            with connection:
                yield connection
        finally:
            connection.close()

    @staticmethod
    def password_hash(password: str, salt: str) -> str:
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt), PASSWORD_ROUNDS
        ).hex()

    @staticmethod
    def token_hash(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def register(self, username: str, password: str) -> dict:
        salt = secrets.token_hex(16)
        digest = self.password_hash(password, salt)
        try:
            with self.connect() as connection:
                cursor = connection.execute(
                    "INSERT INTO users(username, salt, password_hash) VALUES (?, ?, ?)",
                    (username, salt, digest),
                )
                return {"id": cursor.lastrowid, "username": username}
        except sqlite3.IntegrityError as error:
            raise ValueError("Бұл пайдаланушы бұрын тіркелген.") from error

    def login(self, username: str, password: str) -> str | None:
        with self.connect() as connection:
            user = connection.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()
            # Perform the same expensive operation for an unknown username.
            salt = user["salt"] if user else "0" * 32
            digest = self.password_hash(password, salt)
            if user is None or not hmac.compare_digest(user["password_hash"], digest):
                return None
            token = secrets.token_urlsafe(32)
            connection.execute(
                "INSERT INTO sessions(token_hash, user_id, expires) VALUES (?, ?, ?)",
                (self.token_hash(token), user["id"], time.time() + SESSION_SECONDS),
            )
            return token

    def user_for_token(self, token: str) -> dict | None:
        with self.connect() as connection:
            user = connection.execute(
                "SELECT users.id, users.username FROM users JOIN sessions "
                "ON sessions.user_id = users.id "
                "WHERE sessions.token_hash = ? AND sessions.expires > ?",
                (self.token_hash(token), time.time()),
            ).fetchone()
        return dict(user) if user else None

    def logout(self, token: str) -> None:
        with self.connect() as connection:
            connection.execute(
                "DELETE FROM sessions WHERE token_hash = ?", (self.token_hash(token),)
            )
