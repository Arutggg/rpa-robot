import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "robot.db"


@contextmanager
def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_number INTEGER NOT NULL,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                duration_seconds REAL
            )
            """
        )


def create_run(start_number: int, started_at: datetime) -> int:
    with _connect() as conn:
        cursor = conn.execute(
            "INSERT INTO runs (start_number, started_at) VALUES (?, ?)",
            (start_number, started_at.isoformat(timespec="seconds")),
        )
        return cursor.lastrowid


def finish_run(run_id: int, finished_at: datetime, duration: float) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE runs SET finished_at = ?, duration_seconds = ? WHERE id = ?",
            (finished_at.isoformat(timespec="seconds"), round(duration, 2), run_id),
        )


def get_runs() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM runs ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]