
import queue
import threading
import os
from dotenv import load_dotenv

load_dotenv()

_DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER", "fleetuser"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "fleet_manager"),
}

_job_queue: queue.Queue = queue.Queue()
_started = False
_lock = threading.Lock()


def _worker():
    import mysql.connector

    conn = None

    while True:
        job = _job_queue.get()        
        if job is None:                 
            break

        sql, params = job

        try:
            if conn is None or not conn.is_connected():
                conn = mysql.connector.connect(**_DB_CONFIG)

            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            cur.close()

        except Exception as e:
            print(f"[DB_WRITER] Insert failed (non-fatal): {e}")

        finally:
            _job_queue.task_done()


def _ensure_started():
    global _started
    with _lock:
        if not _started:
            t = threading.Thread(target=_worker, daemon=True, name="db-writer")
            t.start()
            _started = True


def log_user(user_id: str, role: str):
    _ensure_started()
    sql = """
        INSERT IGNORE INTO users (user_id, role)
        VALUES (%s, %s)
    """
    _job_queue.put((sql, (user_id, role)))


def log_driver_response(
    driver_id: str,
    trip_id: str,
    segment_index: int,
    severity: str,
    summary: str,
    coaching: str,
):
    _ensure_started()

    
    sql = """
        INSERT INTO driver_responses
            (driver_id, trip_id, segment_index, severity, summary, coaching)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    _job_queue.put((sql, (driver_id, trip_id, segment_index, severity, summary, coaching)))