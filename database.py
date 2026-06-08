import sqlite3
import uuid

DB_FILE = "interview_platform.db"

def init_db():
    """Creates a local database file and sets up the table automatically."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create the table with a version column for Optimistic Locking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_sessions (
            id TEXT PRIMARY KEY,
            status TEXT,
            notes TEXT,
            version INTEGER DEFAULT 1,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def bootstrap_mock_session():
    """Inserts a fresh starting session into our SQLite file."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    session_id = str(uuid.uuid4())
    
    cursor.execute(
        "INSERT INTO interview_sessions (id, status, notes, version) VALUES (?, ?, ?, ?)",
        (session_id, "IN_PROGRESS", "Initial empty baseline canvas.", 1)
    )
    conn.commit()
    conn.close()
    return session_id, 1

# Initialize the database immediately when this file is referenced
init_db()