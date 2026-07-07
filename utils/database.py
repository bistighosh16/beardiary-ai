"""
BearDiary AI - Database Helper 🗄️🐻
SQLite storage for journal entries
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

# Database lives in the project root
DB_PATH = Path(__file__).parent.parent / "beardiary.db"


@contextmanager
def get_connection():
    """Context manager for safe SQLite connections"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # dict-like access to rows
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create the entries table if it doesn't exist"""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT NOT NULL,
                entry_text TEXT NOT NULL,
                mood TEXT,
                mood_emoji TEXT,
                vibe_word TEXT,
                letter TEXT,
                affirmation TEXT,
                created_at TEXT NOT NULL
            )
        """)


def save_entry(
    entry_text: str,
    mood: str,
    mood_emoji: str,
    vibe_word: str,
    letter: str,
    affirmation: str,
    entry_date: str = None
) -> int:
    """Save a new journal entry. Returns the new entry's id."""
    if entry_date is None:
        entry_date = datetime.now().strftime("%Y-%m-%d")
    
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO entries 
            (entry_date, entry_text, mood, mood_emoji, vibe_word, letter, affirmation, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (entry_date, entry_text, mood, mood_emoji, vibe_word, letter, affirmation, created_at))
        
        return cursor.lastrowid


def get_all_entries() -> list:
    """Get all entries, most recent first"""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT * FROM entries ORDER BY created_at DESC
        """).fetchall()
        return [dict(row) for row in rows]


def get_entry_by_id(entry_id: int) -> dict:
    """Get a single entry by ID"""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM entries WHERE id = ?", (entry_id,)).fetchone()
        return dict(row) if row else None


def delete_entry(entry_id: int) -> bool:
    """Delete an entry by ID"""
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
        return cursor.rowcount > 0


def get_mood_stats() -> dict:
    """Get stats: total entries, mood counts, streak, etc."""
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) as c FROM entries").fetchone()["c"]
        
        mood_rows = conn.execute("""
            SELECT mood, COUNT(*) as count 
            FROM entries 
            WHERE mood IS NOT NULL
            GROUP BY mood 
            ORDER BY count DESC
        """).fetchall()
        
        mood_counts = {row["mood"]: row["count"] for row in mood_rows}
        
        return {
            "total_entries": total,
            "mood_counts": mood_counts,
            "top_mood": next(iter(mood_counts), None) if mood_counts else None
        }


def get_entries_for_chart(limit: int = 30) -> list:
    """Get recent entries for mood tracking charts"""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT entry_date, mood, mood_emoji, created_at
            FROM entries 
            WHERE mood IS NOT NULL
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(row) for row in rows]