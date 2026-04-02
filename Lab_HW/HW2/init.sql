-- This file runs automatically when the PostgreSQL container starts for the first time.
-- Add your schema or seed data here.

-- The database is automatically created via POSTGRES_DB.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
