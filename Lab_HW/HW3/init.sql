-- This file runs automatically when the PostgreSQL container starts for the first time.
-- JWT Authentication Lab

-- The database is automatically created via POSTGRES_DB.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
