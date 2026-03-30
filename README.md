🐍 Core Stack
Category 	Technologies
Web Framework 	FastAPI + uvicorn – async REST API
Database 	SQLAlchemy 2.0 (async) + asyncpg + alembic – PostgreSQL with async ORM and migrations
Validation & Config 	Pydantic + pydantic-settings – request/response validation and environment config
Authentication 	python-jose (JWT), passlib (bcrypt/hashing), cryptography – token handling and password security
Utilities 	python-multipart – file upload support (card images?), python-stdnum – possibly for validation of numbers (e.g., tax IDs, not critical)
⚙️ Architecture Notes

    Async‑first – The whole stack (FastAPI, SQLAlchemy, asyncpg) is asynchronous, which fits a game backend where many I/O operations happen concurrently.

    Authentication ready – JWT tokens are implemented (via python-jose) and passwords are hashed (via passlib), so user accounts are secure.

    Database migrations – alembic is included, so schema changes are versioned.
