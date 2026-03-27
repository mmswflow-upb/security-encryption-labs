# Impossible Level PoC

## Goal

Show that impossible level requires both a valid token and the current password — defeating standard CSRF attacks.

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

### 1. Set the security level

1. Open your browser and go to `http://localhost:4280/security.php`
2. Select `impossible` from the dropdown
3. Click `Submit`

### 2. Confirm you are logged in

1. Go to `http://localhost:4280/vulnerabilities/csrf/`
2. You should see the password change form. If you see a login page instead, log in with `admin / password`

### Test A: Missing requirements (expected fail)

This test shows that the server rejects requests without both a valid token and the current password.

Open `csrf_poc_impossible_missing_requirements.html` in the **same browser** where you are logged into DVWA.

How to open the file:

Option A (file manager):
Navigate to `proof-of-concept/impossible/` in your file manager and double-click `csrf_poc_impossible_missing_requirements.html`.

Option B (browser address bar):
Press `Ctrl+O` in your browser, navigate to `proof-of-concept/impossible/`, and select `csrf_poc_impossible_missing_requirements.html`.

Option C (terminal):
```bash
xdg-open proof-of-concept/impossible/csrf_poc_impossible_missing_requirements.html
```

Expected result: DVWA rejects the request. The page either shows an error or does not display `Password Changed.` because the request is missing both the token and the current password.

### Test B: Manual token + current password (controlled success)

This test proves the endpoint works when all required values are provided. In a real attack the attacker cannot obtain the anti-CSRF token (same-origin policy) or the user's current password, which is why this level defeats CSRF.

1. In your browser, go to `http://localhost:4280/vulnerabilities/csrf/`

2. Open the browser's developer tools:
   - Press `F12` or `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (macOS)
   - Or right-click anywhere on the page and select `Inspect`

3. Find the `user_token` value:

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

4. Note the current password for the `admin` user. If you have not changed it, the default is `password`. If you changed it during an earlier test, use whatever you changed it to.

5. Open `csrf_poc_impossible_manual_token.html` in a text editor and make two replacements:

   Find this line:
   ```html
   <input type="hidden" name="user_token" value="IMPOSSIBLE_TOKEN">
   ```
   Replace `IMPOSSIBLE_TOKEN` with the token you copied.

   Find this line:
   ```html
   <input type="hidden" name="password_current" value="CURRENT_PASSWORD">
   ```
   Replace `CURRENT_PASSWORD` with the actual current password (for example `password`).

   Save the file.

6. Immediately open the edited file in the **same browser** where you are logged into DVWA. The token is single-use, so do this quickly.

   How to open: double-click in file manager, or `Ctrl+O` in browser, or:
   ```bash
   xdg-open proof-of-concept/impossible/csrf_poc_impossible_manual_token.html
   ```

Expected result: DVWA shows `Password Changed.` only when both the token and the current password are correct.

### Verify

1. Go to `http://localhost:4280/logout.php`
2. Log in with username `admin` and password `ImpManual123!`
3. If login succeeds, the request was accepted because both checks passed

### Reset the password (optional)

1. Go to `http://localhost:4280/vulnerabilities/csrf/`
2. Type `password` in both fields (and the current password field if present) and click `Change`
