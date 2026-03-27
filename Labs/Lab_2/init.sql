-- This file runs automatically when the PostgreSQL container starts for the first time.
-- Add your schema or seed data here.

-- The database is already created via the POSTGRES_DB env var.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
