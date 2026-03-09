# DVWA Structure Relevant to This Lab

## What This README Is For

This file maps the source files that control database setup and **Cross-Site Request Forgery (CSRF)** behavior in **Damn Vulnerable Web Application (DVWA)**.

The DVWA source is included as a Git submodule at `dvwa-source/`.
Initialize it with:

```bash
git submodule update --init
```

## Runtime Components

- Apache web server (from `dvwa-source/Dockerfile`, based on `php:8-apache`)
- MariaDB 10 database (separate container, see `compose.yml`)
- DVWA PHP code mounted under `/var/www/html` inside the container

The container startup script starts services only. It does not auto-run `setup.php`.

## Important Source Paths

All paths below are relative to `dvwa-source/`.

- `setup.php`
Purpose: handles database creation and reset when `Create / Reset Database` is submitted.

- `config/config.inc.php.dist`
Purpose: template for database credentials and default DVWA settings.
The Dockerfile copies this to `config/config.inc.php` at build time.

- `vulnerabilities/csrf/index.php`
Purpose: dispatches to level-specific logic by reading the security cookie.

- `vulnerabilities/csrf/source/low.php`
- `vulnerabilities/csrf/source/medium.php`
- `vulnerabilities/csrf/source/high.php`
- `vulnerabilities/csrf/source/impossible.php`
Purpose: implement per-level CSRF checks.

## Build Flow (`Dockerfile`)

The `dvwa-source/Dockerfile`:
1. Starts from `php:8-apache`
2. Installs PHP extensions (`gd`, `mysqli`, `pdo`, `pdo_mysql`)
3. Copies the full DVWA source into `/var/www/html`
4. Copies `config/config.inc.php.dist` to `config/config.inc.php`
5. Runs `composer install` for the API module

Our `compose.yml` sets the build context to `./dvwa-source` so Docker builds directly from the submodule.

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

- `dvwa-source/vulnerabilities/csrf/source/low.php`: no anti-CSRF token check
- `dvwa-source/vulnerabilities/csrf/source/medium.php`: weak `Referer` contains server-name check
- `dvwa-source/vulnerabilities/csrf/source/high.php`: requires valid anti-CSRF token
- `dvwa-source/vulnerabilities/csrf/source/impossible.php`: requires valid anti-CSRF token and correct current password
