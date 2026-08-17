from pathlib import Path
import sqlite3

DB_NAME = "tasks.db"
ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "data" / DB_NAME

def get_db_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT NULL
        )
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_tasks_updated_at
            AFTER UPDATE ON tasks
            FOR EACH ROW
            BEGIN
                UPDATE tasks
                SET updated_at = CURRENT_TIMESTAMP
                WHERE id = NEW.id;
            END;
        """)

        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]
        if count == 0:
            default_tasks = [
                ("Complete CN assignment", False),
                ("Write data ingestion logic", False),
                ("Walk the dog", False)
            ]
            cursor.executemany("""
            INSERT INTO tasks (title, done) VALUES (?, ?)
            """,
               default_tasks
            )

        connection.commit()