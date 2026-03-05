# Cross-Site Request Forgery (CSRF)

## What This README Is For

This file explains the CSRF attack model and the defense mechanisms used by each **Damn Vulnerable Web Application (DVWA)** security level (`low`, `medium`, `high`, `impossible`).

## Sessions and Cookies (Foundation)

HyperText Transfer Protocol (HTTP) is stateless by default.  
That means each request is independent unless the application adds state tracking.

### What is a Session

A session is server-side state for a logged-in user.  
The server stores session data (for example user id, role, login timestamp) and links it to a session identifier.

### What is a Cookie

A cookie is small key-value data stored by the browser for a site.  
The browser can automatically attach matching cookies to later requests, based on cookie rules (domain, path, expiry, and security attributes).

### What is a Session Cookie

A session cookie usually stores a session identifier and has no long-term expiry.  
It typically lives until browser close (or until server invalidates it).  
It does not contain your password; it is a pointer to server-side session state.

### Why This Matters for CSRF

In CSRF, attacker code does not need to know your credentials.  
If your browser already has a valid authentication cookie for the target, the browser may send it automatically with a forged request.

## SameSite, Strict, Lax, None

`SameSite` is a cookie attribute that controls when cookies are sent in cross-site contexts.

- `SameSite=Strict`  
Cookie is sent only in same-site contexts. Strong CSRF reduction, but can impact some navigation flows.

- `SameSite=Lax`  
Cookie is sent for same-site requests and limited top-level cross-site navigations (commonly safe `GET` navigations).  
It blocks many cross-site state-changing form submissions.

- `SameSite=None`  
Cookie is allowed in cross-site contexts. Must also include `Secure` (HyperText Transfer Protocol Secure only), or modern browsers reject it.

## What “Standards” These Come From

These behaviors come from the HTTP cookie standard and browser security model:
- Cookie model: Request for Comments (RFC) 6265 family
- Standardization body: Internet Engineering Task Force (IETF)
- `SameSite` behavior: modern browser implementations aligned with the evolving RFC 6265bis work

Practical point: browser defaults and edge behavior can change over time, so test in the browser versions you actually support.

## Core Idea

**Cross-Site Request Forgery (CSRF)** is an attack where a browser sends a state-changing request that the user did not intend.

A typical flow is:
1. User is authenticated on a target site.
2. User opens attacker-controlled content.
3. That content submits a forged request to the target.
4. Browser attaches session cookie.
5. Target accepts the request if anti-CSRF checks are weak or missing.

## Conditions Needed for CSRF

A successful CSRF attack usually needs all of these:
- active authenticated session
- action endpoint that changes server state
- attacker can cause the victim browser to send a matching request shape (method, parameters, headers that are controllable)
- browser policy still sends target authentication cookie in that context (`SameSite` and related rules permit it)
- no strong server-side anti-CSRF validation (token or equivalent)
- no extra step-up checks for the action (for example current password or re-authentication)

## CSRF Prerequisites Checklist (Practical)

Use this quick checklist when evaluating an endpoint:

1. Is the victim typically logged in when visiting external content?
2. Does the endpoint perform state change (`POST`, `GET` misuse, etc.)?
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
