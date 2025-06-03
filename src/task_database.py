
import sqlite3
from sqlite3 import Connection
import os
from time import strftime
from typing import Optional
import logging

logging = logging.getLogger(__name__)

TABLE_NAME = "ScanpyTask"

create_table_query = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    session_id TEXT,
    task_id TEXT NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ipynb TEXT NOT NULL,
    datetime TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now')),
    UNIQUE (task_id)
);
"""

def _ensure_scanpy_task_tables(conn: Optional[Connection]=None):
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
    except Exception as e:
        logging.error(e)
    pass

def _connect_to_db():
    db_path = os.environ.get("DATA_FOLDER", "./data")
    db_path = os.path.join(db_path, "scanpy_task.db")
    if not os.path.exists(db_path):
        try:
            with open(db_path, "w"):
                pass
        except Exception as e:
            logging.error(e)
            return None
    return sqlite3.connect(db_path)

upsert_task_query = f"""
INSERT INTO {TABLE_NAME}(session_id, task_id, ipynb, datetime)
VALUES (?, ?, ?, strftime('%Y-%m-%d %H:%M:%f', 'now'))
ON CONFLICT(task_id) DO UPDATE SET ipynb=excluded.ipynb,
session_id=excluded.session_id,
datetime=strftime('%Y-%m-%d %H:%M:%f', 'now');
"""
def upsert_scanpy_task(
    session_id: str,
    task_id: str,
    ipynb: str
):
    conn = _connect_to_db()
    if conn is None:
        return False
    try:
        _ensure_scanpy_task_tables(conn)
        cursor = conn.cursor()
        cursor.execute(upsert_task_query, (session_id, task_id, ipynb,))
        conn.commit()
        return True
    except Exception as e:
        logging.error(e)
        return False
    finally:
        conn.close()

select_task_query = f"""
SELECT session_id, ipynb, datetime FROM {TABLE_NAME} WHERE task_id = ?;
"""
def select_scanpy_task(task_id: str) -> Optional[dict]:
    conn = _connect_to_db()
    if conn is None:
        return None
    try:
        _ensure_scanpy_task_tables(conn)
        cursor = conn.cursor()
        cursor.execute(select_task_query, (task_id,))
        row = cursor.fetchone()
        if row is not None:
            return {"task_id": task_id, "session_id": row[0], "ipynb": row[1], "datetime": row[2]}
        return None
    except Exception as e:
        logging.error(e)
        return None
    finally:
        conn.close()


