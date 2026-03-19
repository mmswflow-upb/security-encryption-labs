-- This file runs automatically when the MySQL container starts for the first time.
-- Add your schema or seed data here.

CREATE DATABASE IF NOT EXISTS lab_db;
USE lab_db;

-- Example table (adjust for your lab needs)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
