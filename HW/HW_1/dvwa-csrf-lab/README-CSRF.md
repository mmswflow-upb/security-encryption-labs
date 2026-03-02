# Cross-Site Request Forgery (CSRF)

## What It Is

**Cross-Site Request Forgery (CSRF)** is a web attack where a browser sends a request that the user did not intend.

If the user is already signed in to a target site, the browser may include session cookies automatically. The target site may then process the forged request as if the user triggered it.

## Why It Matters

A successful CSRF attack can trigger state-changing actions, for example:
- changing account passwords
- changing account email addresses
- making purchases or money transfers
- changing security settings

## Basic CSRF Attack Flow

1. Victim signs in to a target web application.
2. Victim visits attacker-controlled content.
3. Attacker-controlled content auto-submits a request to the target.
4. Browser includes the victim session cookie.
5. Target accepts request if no strong anti-CSRF protection is enforced.

## Preconditions

CSRF usually needs all of these:
- victim is authenticated to the target
- target endpoint performs a sensitive action
- target endpoint accepts request without strong anti-CSRF validation
- browser sends the session cookie with that request

## Common Defenses

1. Add anti-CSRF tokens and validate them server-side.
2. Use strict cookie policy settings such as `SameSite`, plus `HttpOnly` and `Secure` where appropriate.
3. Avoid state-changing actions over `GET`; use `POST` or stronger patterns.
4. Require user re-authentication for critical operations.
5. Validate `Origin` or `Referer` headers as a secondary check, not as the only check.

## How This Lab Uses CSRF

This lab targets the DVWA password-change function at:
- `/vulnerabilities/csrf/`

At low security level, this endpoint accepts a forged request without anti-CSRF token validation.
