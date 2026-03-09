# High Level PoC

## Security Level Behavior

The server validates an anti-CSRF token (`user_token`) against the current session.
A forged request without a valid token is rejected outright.
A blind CSRF attack that cannot read the token from the victim's page will always fail here.

## Files

- `csrf_poc_high_missing_token.html`
  Intentionally omits `user_token`.
  Use this to confirm the defense blocks incomplete requests.

- `csrf_poc_high_manual_token.html`
  Includes a `user_token` placeholder (`HIGH_TOKEN`).
  Replace it with a real token copied from your active session to demonstrate that the endpoint works when the correct token is present.

## How to Run

### Test A: Missing token (expected fail)

1. Set DVWA security level to `high`
2. Stay logged in
3. Open `proof-of-concept/high/csrf_poc_high_missing_token.html` in the browser
   (use your file manager or browser's open-file dialog to navigate to the repo)

Expected: DVWA rejects the request with a token error.

### Test B: Manual valid token (controlled success)

1. Open `http://localhost:8081/vulnerabilities/csrf/` in browser
2. Inspect the form source and copy the `user_token` value
3. Edit `csrf_poc_high_manual_token.html` and replace `HIGH_TOKEN` with the copied value
4. Open `proof-of-concept/high/csrf_poc_high_manual_token.html` in the browser immediately (token is single-use)
   (use your file manager or browser's open-file dialog to navigate to the repo)

Expected: DVWA shows `Password Changed.`

## Verify

Login with `HighManual123!` after a successful Test B.
