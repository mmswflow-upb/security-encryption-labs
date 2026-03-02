# Damn Vulnerable Web Application (DVWA) Structure

## Purpose

**Damn Vulnerable Web Application (DVWA)** is a training application that intentionally contains vulnerabilities.

This lab focuses on the CSRF module, but understanding the related file layout helps explain behavior by security level.

## Container-Level Structure Used in This Lab

The Docker image serves the web application from:
- `/var/www/html/`

Important CSRF paths:
- `/var/www/html/vulnerabilities/csrf/index.php`
- `/var/www/html/vulnerabilities/csrf/source/low.php`
- `/var/www/html/vulnerabilities/csrf/source/medium.php`
- `/var/www/html/vulnerabilities/csrf/source/high.php`
- `/var/www/html/vulnerabilities/csrf/source/impossible.php`

## CSRF Module Request Flow

1. `index.php` loads the current security level from cookie `security`.
2. It includes one source file based on level: `low.php`, `medium.php`, `high.php`, or `impossible.php`.
3. Each source file handles request validation and password update logic differently.

## Security Level Behavior Summary

### Low
- Accepts `GET` request with `password_new`, `password_conf`, and `Change`.
- No anti-CSRF token check.
- Vulnerable to simple forged requests.

### Medium
- Same parameters as low.
- Adds a check based on the `Referer` header containing server name.
- Weak defense, because `Referer` can be missing or bypassed in some setups.

### High
- Requires anti-CSRF token via `user_token`.
- Generates session token server-side and validates per request.
- A naive forged request without token fails.

### Impossible
- Requires anti-CSRF token and current password (`password_current`).
- Adds strict validation and better update flow.
- Strongest level among DVWA CSRF options.

## Why This Matters for the Lab

The same endpoint can behave very differently only by switching security level. This is why your testing must cover low, medium, high, and impossible, not only low.
