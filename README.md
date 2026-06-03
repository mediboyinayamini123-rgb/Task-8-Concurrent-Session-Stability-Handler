# Task 8: Concurrent Session Stability handler

## Project Overview
The main purpose of this project is to provide a robust FastAPI backend that handles multi-user interview data safely, using version-checking logic to completely eliminate database data corruption and race conditions.
Race Condition Mitigation: Prevents "Lost Update" bugs by making sure two interviewers saving data at the exact same millisecond cannot accidentally overwrite each other's work.
Optimistic Concurrency Control: Catches overlapping saves at the same millisecond and safely blocks them with a 409 Concurrency Conflict error.
Isolated Workspace Tracking: Manages session records cleanly in a local SQLite database using a permanent workspace identity token ("uptoskills").
Asynchronous Background Processing: Offloads heavy analytical workflows to background workers to ensure the user interface never experiences lag.

## Tech Stack & Dependencies
Language: Python 3 — The core programming language used to write the application backend logic.

Framework: FastAPI — A modern, high-performance web framework used to build the RESTful API endpoints.

ASGI Server: Uvicorn — The lightning-fast web server engine used to run and deploy the FastAPI application locally.

Database: SQLite — A lightweight, file-based SQL database engine used to store and manage candidate session records safely.

## Repository File Structure
database.py — Manages the SQLite connection pool, initializes the database tables, and handles session cleanup tasks.
interview_platform.db — The standalone, local SQLite database file. This file is created automatically by Python the moment the server boots up and runs the SQL database initialization code.
main.py — The central application file housing the FastAPI initialization, the REST endpoints, and the background task hooks.
test_concurrency.py — The client testing script that fires simultaneous multi-threaded requests to verify the locking engine.

##  How to Setup and Run the Project
Step 1: Initialize the Web Server Engine (Terminal 1)
Run this command in your first terminal window to launch your FastAPI server locally using Uvicorn:

```Bash
uvicorn main:app --reload
