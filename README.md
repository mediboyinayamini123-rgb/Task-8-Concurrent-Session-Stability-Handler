# Concurrent Session Stability Handler

## Overview

This project implements a concurrency-safe interview session management system using FastAPI, SQLite, and Python's asynchronous programming capabilities.

The primary objective is to safely handle multiple simultaneous interview updates while preventing race conditions, maintaining session isolation, and ensuring data consistency.

The solution demonstrates:

* Concurrency control using Optimistic Locking
* Session isolation through unique session identifiers
* Race condition detection and prevention
* Background task processing
* Concurrent request testing using asyncio and httpx

---

## Problem Statement

In an interview platform, multiple requests may attempt to update the same interview session simultaneously.

Without proper concurrency control, this can lead to:

* Lost updates
* Data corruption
* Overwritten interview notes
* Inconsistent interview status
* Duplicate submissions

This project solves these challenges using version-based optimistic locking.

---

## Features

### Session Management

* Create interview sessions dynamically
* Unique UUID-based session identifiers
* Session status tracking

### Session Isolation

* Request validation using X-Session-ID header
* Prevents cross-session data contamination
* Ensures users can only modify their own session

### Optimistic Locking

* Version-based concurrency control
* Prevents stale updates
* Detects concurrent modifications

### Race Condition Prevention

* Only one update can succeed for a given version
* Remaining conflicting requests receive HTTP 409 Conflict

### Background Processing

* Asynchronous report generation
* Non-blocking execution using FastAPI BackgroundTasks

### Concurrency Testing

* Simulates multiple simultaneous updates
* Verifies race condition handling
* Demonstrates conflict detection

---

## Technology Stack

* Python 3.x
* FastAPI
* Uvicorn
* SQLite
* Asyncio
* HTTPX

---

## Project Structure

```text
pure_python_project/
│
├── database.py
├── main.py
├── test_concurrency.py
├── interview_platform.db
└── README.md
```

---

## Database Schema

Table: interview_sessions

| Column     | Type     | Description                |
| ---------- | -------- | -------------------------- |
| id         | TEXT     | Unique session identifier  |
| status     | TEXT     | Interview status           |
| notes      | TEXT     | Interview notes            |
| version    | INTEGER  | Optimistic locking version |
| updated_at | DATETIME | Last update timestamp      |

---

## How Optimistic Locking Works

Every session contains a version field.

Example:

```text
Version = 1
```

Three concurrent requests attempt to update:

```text
Request A -> Version 1
Request B -> Version 1
Request C -> Version 1
```

The first request succeeds:

```text
Version becomes 2
```

The remaining requests fail because they still expect:

```text
Version = 1
```

Result:

```text
1 Successful Update
2 Conflict Responses
```

This prevents race conditions and data corruption.

---

## Installation
Install dependencies:

```bash
pip install fastapi uvicorn httpx
```

---

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

The application will automatically create:

```text
interview_platform.db
```

---

## Running the Concurrency Test

Open a second terminal and execute:

```bash
python test_concurrency.py
```

---

## Expected Output

```text
Session setup with ID: xxxxx

Request #1 Return Code: 200
Payload Output:
{
  "version": 2
}

Request #2 Return Code: 409
Payload Output:
{
  "error": "CONCURRENCY_CONFLICT"
}

Request #3 Return Code: 409
Payload Output:
{
  "error": "CONCURRENCY_CONFLICT"
}
```

---
## Sample Test Result
1. Constructing sample interview data state inside local SQLite database...
   
Session setup with ID: b7a9cf40-487b-4205-b260-36a167a9a065 | Starting Version: 1

3. Dispatching 3 concurrent updates to the same version state at the same millisecond...

4. Testing execution matrix feedback:
   
Request #1 Return Code: 200

Payload Output: {"id":"b7a9cf40-487b-4205-b260-36a167a9a065","status":"IN_PROGRESS","notes":"Interviewer A notes","version":2}

Request #2 Return Code: 409

Payload Output: {"detail":{"error":"CONCURRENCY_CONFLICT","message":"The session state has changed. Please refresh your data and try again."}}

Request #3 Return Code: 409

Payload Output: {"detail":{"error":"CONCURRENCY_CONFLICT","message":"The session state has changed. Please refresh your data and try again."}}




