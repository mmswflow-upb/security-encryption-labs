# Low Level PoC

## Goal

Demonstrate a successful CSRF password change on low level.

## Security Level Behavior

No anti-CSRF protection is present at this level.
The server accepts the password change request if `password_new` equals `password_conf`.

## Files

- `csrf_poc_low.html`
  Submits a forged GET request with new credentials.
  No token, no current password, no header validation required.

## Expected Result

DVWA shows `Password Changed.`
Login with `NewPass123!` succeeds after the attack.

## How to Run

1. In DVWA, open `DVWA Security` and set level to `low`, then click `Submit`
2. Ensure you are still logged in as `admin`
3. Open `proof-of-concept/low/csrf_poc_low.html` in the browser
   (use your file manager or browser's open-file dialog to navigate to the repo)
4. Return to DVWA and check the CSRF page for `Password Changed.`
5. Verify by logging out and back in with `NewPass123!`
