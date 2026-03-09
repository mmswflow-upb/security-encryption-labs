# Proof of Concept (PoC) Files

## What This README Is For

This file explains each **Proof of Concept (PoC)** file, required inputs, and expected outcome per **Damn Vulnerable Web Application (DVWA)** security level.

## Folder Structure

PoC files are organized under `proof-of-concept/` by security level:

```
proof-of-concept/
  low/
    csrf_poc_low.html
    README.md
  medium/
    csrf_poc_medium.html
    README.md
  high/
    csrf_poc_high_missing_token.html
    csrf_poc_high_manual_token.html
    README.md
  impossible/
    csrf_poc_impossible_missing_requirements.html
    csrf_poc_impossible_manual_token.html
    README.md
```

Each level folder has its own `README.md` with full run instructions and expected results.

## Endpoint and Common Fields

All PoC files target:
- `http://localhost:8081/vulnerabilities/csrf/`

Common request fields used by DVWA:
- `password_new`
- `password_conf`
- `Change`

Additional fields required at stronger levels:
- `user_token` (high and impossible)
- `password_current` (impossible)

## File-by-File Reference

- `proof-of-concept/low/csrf_poc_low.html`
Use for: low level baseline test.
Expected: success on low level.

- `proof-of-concept/medium/csrf_poc_medium.html`
Use for: medium level test.
Expected: depends on whether request passes weak `Referer` check.

- `proof-of-concept/high/csrf_poc_high_missing_token.html`
Use for: negative test on high level.
Expected: fail because `user_token` is missing.

- `proof-of-concept/high/csrf_poc_high_manual_token.html`
Use for: controlled high-level test with manually inserted `user_token`.
Expected: can succeed only when token is valid for current session.

- `proof-of-concept/impossible/csrf_poc_impossible_missing_requirements.html`
Use for: negative test on impossible level.
Expected: fail because required controls are not satisfied.

- `proof-of-concept/impossible/csrf_poc_impossible_manual_token.html`
Use for: controlled impossible-level test.
Expected: can succeed only with both valid `user_token` and correct `password_current`.

## Why Two Files for High and Impossible

Each of those levels has:
- one expected-fail file that proves the defense blocks incomplete requests
- one manual file that demonstrates what exact protected inputs are required

## Practical Testing Notes

1. Stay logged in while opening PoC files.
2. Use the same browser profile and tab session.
3. For token-based tests, copy token from live DVWA form immediately before test.
4. Verify result by logging out and logging back in with expected password.
