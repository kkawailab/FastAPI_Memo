# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple memo/note-taking application built with FastAPI. The application provides a REST API for creating, reading, updating, deleting, and searching memos. All documentation and user-facing messages are in Japanese.

## Essential Commands

### Development Server
```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server with auto-reload
uvicorn main:app --reload

# Run on a specific port
uvicorn main:app --reload --port 8080
```

### API Documentation
- Interactive API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

## Architecture

The application follows a simple monolithic architecture with all code in a single `main.py` file:

1. **Database Layer**: SQLAlchemy ORM with SQLite
   - Database URL: `sqlite:///./memo_app.db` (created automatically)
   - Single table: `memos` with columns: id, title, content, created_at, updated_at

2. **API Layer**: FastAPI with Pydantic models
   - Request/Response validation using Pydantic models
   - CORS enabled for all origins (development configuration)
   - No authentication/authorization implemented

3. **Data Models**:
   - `Memo`: SQLAlchemy model for database
   - `MemoBase`, `MemoCreate`, `MemoUpdate`, `MemoResponse`: Pydantic models for API

## API Endpoints

- `GET /` - Welcome message
- `POST /memos/` - Create a new memo
- `GET /memos/` - List all memos (with pagination: skip, limit)
- `GET /memos/{memo_id}` - Get specific memo
- `PUT /memos/{memo_id}` - Update memo (partial updates supported)
- `DELETE /memos/{memo_id}` - Delete memo
- `GET /memos/search/?q={query}` - Search memos by title or content

## Development Notes

- The database file (`memo_app.db`) is created automatically in the project directory
- All error messages and API responses are in Japanese
- The application uses SQLite with `check_same_thread=False` for development
- No testing infrastructure is currently implemented
- No environment configuration files - database URL is hardcoded