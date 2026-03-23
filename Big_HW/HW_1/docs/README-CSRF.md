# Cross-Site Request Forgery (CSRF)

## What This README Is For

This file explains the CSRF attack model and the defense mechanisms used by each DVWA (Damn Vulnerable Web Application) security level.

For foundational concepts (sessions, cookies, local storage, JWTs, SameSite), see [README-WEB-SECURITY-BASICS.md](README-WEB-SECURITY-BASICS.md).

## Core Idea

CSRF is an attack where a browser sends a state-changing request that the user did not intend.

A typical flow:

1. User is authenticated on a target site
2. User opens attacker-controlled content (a malicious page, email link, etc.)
3. That content submits a forged request to the target
4. Browser attaches session cookie automatically
5. Target accepts the request if anti-CSRF checks are weak or missing

The attacker does not need to know the victim's credentials.
The browser already has a valid session cookie for the target and sends it automatically with the forged request.

## Conditions Needed for CSRF

A successful CSRF attack usually needs all of these:

- active authenticated session
- action endpoint that changes server state
- attacker can cause the victim browser to send a matching request shape (method, parameters, headers that are controllable)
- browser policy still sends target authentication cookie in that context (SameSite and related rules permit it)
- no strong server-side anti-CSRF validation (token or equivalent)
- no extra step-up checks for the action (for example current password or re-authentication)

## CSRF Prerequisites Checklist

Use this quick checklist when evaluating an endpoint:

1. Is the victim typically logged in when visiting external content?
2. Does the endpoint perform state change (POST, GET misuse, etc.)?
3. Can attacker-controlled content trigger that request from a browser?
4. Will authentication cookies be sent in that cross-site context?
5. Is there a validated anti-CSRF token tied to the victim session?
6. Is there additional confirmation (current password, one-time challenge, re-login)?

## DVWA CSRF Module: What Changes by Level

Target endpoint in this lab:
- `/vulnerabilities/csrf/`

Required input fields in base form:
- `password_new`
- `password_conf`
- `Change`

### Low Level Mechanism

Protection used:
- none

Server behavior:
- accepts request and changes password if `password_new == password_conf`

Security impact:
- classic CSRF is straightforward

### Medium Level Mechanism

Protection used:
- checks whether `Referer` header contains server name

Server behavior:
- rejects if `Referer` is missing or does not match
- accepts if weak `Referer` condition passes

Security impact:
- this is weak because header-based origin checks are not a robust anti-CSRF control

### High Level Mechanism

Protection used:
- anti-CSRF token (`user_token`) validated against session token

Server behavior:
- rejects forged request without valid token
- accepts only if token matches current authenticated session

Security impact:
- naive blind CSRF fails

### Impossible Level Mechanism

Protection used:
- anti-CSRF token validation
- current password verification (`password_current`)

Server behavior:
- requires both valid token and correct current password

Security impact:
- strongest protection in DVWA CSRF levels

## Why Your Proof of Concept Results Differ by Level

- `low`: succeeds with simple auto-submit
- `medium`: may fail from `file://` and may pass in some same-host setups due to weak `Referer` logic
- `high`: fails without valid token
- `impossible`: fails without valid token and correct current password

## Defensive Guidance for Real Systems

Use layered controls:
1. unpredictable anti-CSRF token per request or per session with strict server validation
2. cookie policy with `SameSite`, plus `HttpOnly` and `Secure` where appropriate
3. avoid state-changing operations on `GET`
4. step-up authentication for critical actions
5. treat `Referer` and `Origin` checks as secondary controls, not primary protection
