# Impossible Level PoC

## Security Level Behavior

The server requires both:
- a valid anti-CSRF token (`user_token`) matching the current session
- the correct current password (`password_current`) for the authenticated user

Both checks must pass simultaneously.
This is the strongest protection in DVWA's CSRF levels and defeats standard CSRF attacks entirely.

## Files

- `csrf_poc_impossible_missing_requirements.html`
  Omits both `user_token` and `password_current`.
  Use this to confirm the defense rejects incomplete requests.

- `csrf_poc_impossible_manual_token.html`
  Includes placeholders for both required values (`IMPOSSIBLE_TOKEN`, `CURRENT_PASSWORD`).
  Replace them manually to demonstrate what is required for the request to succeed.

## How to Run

### Test A: Missing requirements (expected fail)

1. Set DVWA security level to `impossible`
2. Stay logged in
3. Open `proof-of-concept/impossible/csrf_poc_impossible_missing_requirements.html` in the browser
   (use your file manager or browser's open-file dialog to navigate to the repo)

Expected: DVWA rejects the request.

### Test B: Manual token + current password (controlled success)

1. Open `http://localhost:8081/vulnerabilities/csrf/` in browser
2. Copy the `user_token` value from the form source
3. Note the current password for the logged-in user
4. Edit `csrf_poc_impossible_manual_token.html`:
   - Replace `IMPOSSIBLE_TOKEN` with the copied token
   - Replace `CURRENT_PASSWORD` with the actual current password
5. Open `proof-of-concept/impossible/csrf_poc_impossible_manual_token.html` in the browser immediately
   (use your file manager or browser's open-file dialog to navigate to the repo)

Expected: DVWA shows `Password Changed.` only when both values are correct.

## Verify

Login with `ImpManual123!` after a successful Test B.
