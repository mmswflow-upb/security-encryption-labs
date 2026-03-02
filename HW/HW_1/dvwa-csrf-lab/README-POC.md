# Proof of Concept (PoC) Guide

This guide targets **Damn Vulnerable Web Application (DVWA)** and its **Cross-Site Request Forgery (CSRF)** module.

## What a PoC Means Here

A **Proof of Concept (PoC)** is a minimal reproducible artifact that demonstrates behavior.

In this lab, each PoC is a local Hypertext Markup Language (HTML) file that submits a request to DVWA's CSRF endpoint.

## PoC Files

- `csrf_poc.html`: Baseline forged request, useful for low level.
- `csrf_poc_medium.html`: Same request, used to test medium level behavior.
- `csrf_poc_high_missing_token.html`: High-level request without token, expected to fail.
- `csrf_poc_high_manual_token.html`: High-level template where you insert a real token manually.
- `csrf_poc_impossible_missing_requirements.html`: Impossible-level request missing required fields, expected to fail.
- `csrf_poc_impossible_manual_token.html`: Impossible-level template where you insert current password and token manually.

## Level Matrix

| Security level | File | Expected result | Why |
|---|---|---|---|
| low | `csrf_poc.html` | Password changes | No anti-CSRF token check |
| medium | `csrf_poc_medium.html` | Depends on `Referer` handling | Weak `Referer`-based check |
| high | `csrf_poc_high_missing_token.html` | Fails | Missing `user_token` |
| high | `csrf_poc_high_manual_token.html` | Can succeed in controlled same-session test | Valid `user_token` supplied manually |
| impossible | `csrf_poc_impossible_missing_requirements.html` | Fails | Missing current password and token validation context |
| impossible | `csrf_poc_impossible_manual_token.html` | Can succeed only with current password and valid token | Requires both token and current password |

## How to Test Across Levels

1. Sign in to DVWA.
2. Set security level in `DVWA Security`.
3. Open matching PoC file.
4. Observe response message on `/vulnerabilities/csrf/`.
5. Confirm by signing out and signing in with expected password.

## Important Practical Note

For medium level, browser `Referer` behavior can affect the result:
- Opening from `file:///...` may omit `Referer` and fail.
- Serving PoC over `http://localhost:<port>/...` may satisfy weak checks that only look for `localhost`.

## Why High and Impossible Templates Are Useful

They show that simple forged requests are no longer enough. You need values that an external attacker should not be able to obtain safely, such as anti-CSRF token and current password.
