import sqlite3
import asyncio
from fastapi import FastAPI, HTTPException, Header, status, BackgroundTasks
from database import DB_FILE, bootstrap_mock_session

app = FastAPI()

async def heavy_analytical_report_task(session_id: str):
    """Replaces Celery. Runs a heavy task completely in the background of Python."""
    print(f"\n[Background Worker] Commencing heavy analysis matrix for session: {session_id}")
    
    # Simulate a heavy 4-second operation (AI parsing, scorecard compilation)
    await asyncio.sleep(4)
    
    print(f"[Background Worker] Analysis successfully generated for session: {session_id}\n")

@app.post("/api/sessions/bootstrap")
def bootstrap():
    session_id, version = bootstrap_mock_session()
    return {"id": session_id, "status": "IN_PROGRESS", "notes": "Initial empty baseline canvas.", "version": version}

@app.put("/api/sessions/{session_id}")
async def update_session(
    session_id: str, 
    payload: dict, 
    background_tasks: BackgroundTasks,
    x_session_id: str = Header(None)
):
    # Context Isolation Check
    if not x_session_id or x_session_id != session_id:
        raise HTTPException(status_code=400, detail="Missing or cross-contaminated Session ID Header.")

    notes = payload.get("notes", "")
    new_status = payload.get("status", "IN_PROGRESS")
    current_version = payload.get("currentVersion")

    if current_version is None:
        raise HTTPException(status_code=400, detail="currentVersion property is mandatory.")

    # Connect to the local SQLite file
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # OPTIMISTIC LOCKING: Check if version matches before modifying rows
    cursor.execute(
        """
        UPDATE interview_sessions 
        SET notes = ?, status = ?, version = version + 1, updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND version = ?
        """,
        (notes, new_status, session_id, current_version)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    # If 0 rows were updated, a race condition occurred! Trigger a 409 Conflict
    if rows_affected == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "CONCURRENCY_CONFLICT",
                "message": "The session state has changed. Please refresh your data and try again."
            }
        )

    # If session is marked COMPLETED, offload the task using FastAPI's built-in background engine
    if new_status == "COMPLETED":
        background_tasks.add_task(heavy_analytical_report_task, session_id)

    return {"id": session_id, "status": new_status, "notes": notes, "version": current_version + 1}