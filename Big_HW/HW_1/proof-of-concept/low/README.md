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

### 1. Set the security level

1. Open your browser and go to `http://localhost:4280/security.php`
2. Select `low` from the dropdown
3. Click `Submit`

### 2. Confirm you are logged in

1. Go to `http://localhost:4280/vulnerabilities/csrf/`
2. You should see the password change form. If you see a login page instead, log in with `admin / password`

### 3. Open the PoC file

Open `csrf_poc_low.html` in the **same browser** where you are logged into DVWA.
The browser must be the same so it sends the DVWA session cookie with the forged request.

How to open the file:

Option A (file manager):
Navigate to `proof-of-concept/low/` in your file manager and double-click `csrf_poc_low.html`. It opens in your default browser.

Option B (browser address bar):
Press `Ctrl+O` in your browser, navigate to the `proof-of-concept/low/` folder, and select `csrf_poc_low.html`.

Option C (terminal):
```bash
xdg-open proof-of-concept/low/csrf_poc_low.html
```
On macOS use `open` instead of `xdg-open`. On Windows use `start`.

The page auto-submits the form immediately on load. You should see the DVWA CSRF page with `Password Changed.` in the response.

### 4. Verify the password was changed

1. Go to `http://localhost:4280/logout.php`
2. Log in with username `admin` and password `NewPass123!`
3. If login succeeds, the CSRF attack worked

### 5. Reset the password (optional)

To restore the original password:
1. Go to `http://localhost:4280/vulnerabilities/csrf/`
2. Type `password` in both fields and click `Change`
