# High Level PoC

## Goal

Show the difference between a missing token (blocked) and a valid token (passes) at high level.

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

### 1. Set the security level

1. Open your browser and go to `http://localhost:4280/security.php`
2. Select `high` from the dropdown
3. Click `Submit`

### 2. Confirm you are logged in

1. Go to `http://localhost:4280/vulnerabilities/csrf/`
2. You should see the password change form. If you see a login page instead, log in with `admin / password`

### Test A: Missing token (expected fail)

This test shows that the server rejects requests without a valid anti-CSRF token.

Open `csrf_poc_high_missing_token.html` in the **same browser** where you are logged into DVWA.

How to open the file:

Option A (file manager):
Navigate to `proof-of-concept/high/` in your file manager and double-click `csrf_poc_high_missing_token.html`.

Option B (browser address bar):
Press `Ctrl+O` in your browser, navigate to `proof-of-concept/high/`, and select `csrf_poc_high_missing_token.html`.

Option C (terminal):
```bash
xdg-open proof-of-concept/high/csrf_poc_high_missing_token.html
```

Expected result: DVWA rejects the request. The page either shows an error or does not display `Password Changed.` because the request has no valid `user_token`.

### Test B: Manual valid token (controlled success)

This test proves the endpoint works when a valid token is provided. In a real attack the attacker cannot obtain this token (the browser's same-origin policy prevents reading another site's page content), but here we copy it manually to demonstrate the mechanism.

1. In your browser, go to `http://localhost:4280/vulnerabilities/csrf/`

2. Open the browser's developer tools:
   - Press `F12` or `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (macOS)
   - Or right-click anywhere on the page and select `Inspect`

3. Find the `user_token` value. Two ways:

   Using the Elements/Inspector tab:
   - Press `Ctrl+F` (or `Cmd+F` on macOS) to search within the HTML
   - Type `user_token` and press Enter
   - Find the hidden input: `<input type="hidden" name="user_token" value="...">`
   - Copy the value inside the `value="..."` attribute

   Using the Console tab:
   - Click the Console tab
   - Paste this and press Enter:
     ```javascript
     document.querySelector('input[name="user_token"]').value
     ```
   - Copy the output string

4. Open `csrf_poc_high_manual_token.html` in a text editor and find this line:
   ```html
   <input type="hidden" name="user_token" value="HIGH_TOKEN">
   ```
   Replace `HIGH_TOKEN` with the token you copied. Save the file.

5. Immediately open the edited file in the **same browser** where you are logged into DVWA. The token is single-use, so do this quickly before navigating to any other DVWA page (which would regenerate the token).

   How to open: double-click in file manager, or `Ctrl+O` in browser, or:
   ```bash
   xdg-open proof-of-concept/high/csrf_poc_high_manual_token.html
   ```

Expected result: DVWA shows `Password Changed.`

### Verify

1. Go to `http://localhost:4280/logout.php`
2. Log in with username `admin` and password `HighManual123!`
3. If login succeeds, the request was accepted because the token was valid

### Reset the password (optional)

1. Go to `http://localhost:4280/vulnerabilities/csrf/`
2. Type `password` in both fields and click `Change`
