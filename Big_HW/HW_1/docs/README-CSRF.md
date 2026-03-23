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

## Referer Header

When your browser sends a request, it often includes a `Referer` header that tells the server which page you were on when the request was made.

For example, if you are on `https://attacker.com/evil.html` and that page submits a form to `https://example.com/change-password`, the request will include:

```
Referer: https://attacker.com/evil.html
```

The server can read this header and check whether the request came from its own site or from somewhere else.
If the Referer does not match the server's own domain, the server can reject the request.

Why this is a weak defense:
- The Referer header can be missing entirely. Some browsers, privacy extensions, or network configurations strip it out. The server then has to decide whether to allow or reject requests with no Referer, and either choice has problems.
- The check is only as good as how strictly the server validates it. A loose check like "does the Referer contain my server name somewhere" can be tricked (for example, an attacker could host their page at `https://attacker.com/example.com/evil.html` and the server name would appear in the Referer).
- It is not a cryptographic proof of anything. It is just a header the browser fills in, and certain request types or browser settings may omit or alter it.

## Anti-CSRF Tokens

An anti-CSRF token is a secret, unpredictable value that the server generates and embeds in the page.
When the user submits a form, the token is sent along with the request. The server checks whether the token matches what it expects for that user's session.

The flow:

1. The server generates a random token and stores it in the user's session
2. The server includes that token as a hidden field in the HTML form it sends to the browser
3. When the user submits the form, the token is sent along with the other form data
4. The server compares the submitted token against the one stored in the session
5. If they match, the request is legitimate. If they do not match (or the token is missing), the server rejects the request.

Why this stops CSRF:
The attacker can make your browser send cookies automatically, but the attacker cannot read the contents of a page on the target site (the browser's same-origin policy prevents this).
Since the attacker cannot read the page, they cannot see the token value, and therefore cannot include a valid token in their forged request.

Why this is a strong defense:
- It is a cryptographic-strength random value, not something an attacker can guess
- It is tied to the user's specific session, so a token from one session is useless in another
- It does not rely on browser behavior or headers that might be stripped or spoofed

Limitations:
- The server must correctly generate, embed, and validate the token on every state-changing endpoint
- If the application has an XSS vulnerability, an attacker's injected script can read the token from the page and include it in the forged request, bypassing this defense entirely

## One-Time Challenges

A one-time challenge is any extra verification step that requires the user to prove something right now, in a way that an attacker cannot predict or replay.

Common examples:

Current password re-entry:
The application asks you to type your current password before allowing a sensitive action like changing your password or email. An attacker forging a request cannot know your password, so the forged request fails. This is what DVWA's impossible level does.

CAPTCHA:
A visual or interactive puzzle (like "click all the traffic lights") that proves a human is performing the action, not an automated script. An attacker's auto-submitting HTML page cannot solve a CAPTCHA.

Email or SMS confirmation codes:
The server sends a random code to your email or phone and you have to type it back. The attacker has no access to your inbox or phone, so they cannot complete the action.

Re-authentication:
Instead of just asking for a password, some applications make you go through the full login flow again before performing critical actions. This is common for things like deleting an account or changing payment information.

One-time password from an authenticator app:
A time-based code generated by an app like Google Authenticator. The code changes every 30 seconds and the attacker does not have access to the app.

What they all have in common: the server requires a piece of information that only the real, present user can provide at that moment. A forged request from an attacker's page cannot include it because the attacker does not have access to the user's password, phone, email, or physical presence.

The trade-off is usability. You cannot ask users to solve a CAPTCHA or re-enter their password on every single action. That is why these challenges are typically reserved for high-impact actions like password changes, account deletion, or financial transactions.

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
