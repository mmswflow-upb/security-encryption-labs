# DVWA Structure Relevant to This Lab

## What This README Is For

This file maps the source files that control database setup and **Cross-Site Request Forgery (CSRF)** behavior in **Damn Vulnerable Web Application (DVWA)**.

## Runtime Components in This Docker Image

- Apache web server
- MySQL or MariaDB database server
- DVWA PHP (Hypertext Preprocessor) code under `/var/www/html`

Container startup script (`/main.sh`) starts services only. It does not auto-run `setup.php` database reset.

## Important Paths

- `setup.php`
Purpose: handles database creation and reset when `Create / Reset Database` is submitted.

- `config/config.inc.php`
Purpose: database credentials, default DVWA settings, default security level.

- `vulnerabilities/csrf/index.php`
Purpose: dispatches to level-specific logic by reading security cookie.

- `vulnerabilities/csrf/source/low.php`
- `vulnerabilities/csrf/source/medium.php`
- `vulnerabilities/csrf/source/high.php`
- `vulnerabilities/csrf/source/impossible.php`
Purpose: implement per-level CSRF checks.

## Setup Flow (`setup.php`)

1. Load setup page and anti-CSRF token.
2. On `create_db` submission, validate token.
3. Include database setup code (`dvwa/includes/DBMS/MySQL.php`).
4. Drop and recreate `dvwa` database.
5. Create required tables.
6. Insert seed data, including `admin / password` user.

This is why setup is mandatory before running tests.

## CSRF Flow (`vulnerabilities/csrf/index.php`)

1. Read current security level from cookie `security`.
2. Include matching level source file.
3. Evaluate incoming request.
4. If checks pass, update password for current authenticated user.

## Quick Mapping: Security Level to Implementation Rule

- `low.php`: no anti-CSRF token check
- `medium.php`: weak `Referer` contains server-name check
- `high.php`: requires valid anti-CSRF token
- `impossible.php`: requires valid anti-CSRF token and correct current password
