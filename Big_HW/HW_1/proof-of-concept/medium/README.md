# Medium Level PoC

## Goal

Run medium-level CSRF checks and see the effect of `Referer` validation.

## Security Level Behavior

The server checks whether the `Referer` header contains the server name.
This is a weak control: no cryptographic token is used, and the check can be bypassed by serving the PoC from a same-host origin.

## Files

- `csrf_poc_medium.html`
  Same forged GET request as low level.
  Behavior depends on how and where the file is opened.

## How to Run

### 1. Set the security level

1. Open your browser and go to `http://localhost:4280/security.php`
2. Select `medium` from the dropdown
3. Click `Submit`

### 2. Confirm you are logged in

1. Go to `http://localhost:4280/vulnerabilities/csrf/`
2. You should see the password change form. If you see a login page instead, log in with `admin / password`

### Test A: Open from `file://` (expected fail)

This test shows that the Referer check blocks requests from local files.

Open `csrf_poc_medium.html` in the **same browser** where you are logged into DVWA.

How to open the file:

Option A (file manager):
Navigate to `proof-of-concept/medium/` in your file manager and double-click `csrf_poc_medium.html`.

Option B (browser address bar):
Press `Ctrl+O` in your browser, navigate to `proof-of-concept/medium/`, and select `csrf_poc_medium.html`.

Option C (terminal):
```bash
xdg-open proof-of-concept/medium/csrf_poc_medium.html
```

Expected result: DVWA shows `That request didn't look correct.` because the browser sends no `Referer` header when a page is opened from a local file (`file://` protocol). The server sees no Referer, fails the check, and rejects the request.

### Test B: Serve from localhost (expected pass)

This test shows that the weak Referer check can be bypassed. When we serve the PoC from `http://localhost`, the browser sets the Referer to a URL containing "localhost", which is the same server name DVWA checks for.

Important: VS Code Live Server will not work for this test. It serves on `http://127.0.0.1:5500`, and the string "localhost" does not appear in that URL. DVWA checks for the string "localhost" specifically, so the Referer check would still fail. You need to serve on an explicit `localhost` hostname.

1. Open a terminal and navigate to the `HW_1` folder (the project root)

2. Start a Python HTTP server:

Linux / macOS:
```bash
python3 -m http.server 8082
```

Windows (PowerShell):
```powershell
py -m http.server 8082
```

This serves the current directory at `http://localhost:8082`.

3. In the **same browser** where you are logged into DVWA, go to:
```
http://localhost:8082/proof-of-concept/medium/csrf_poc_medium.html
```

4. The page auto-submits. The browser sets the Referer header to `http://localhost:8082/proof-of-concept/medium/csrf_poc_medium.html`, which contains the string "localhost". DVWA's weak check passes and the password changes.

5. Stop the Python server with `Ctrl+C` in the terminal when done.

### Verify

If the password changed in Test B:
1. Go to `http://localhost:4280/logout.php`
2. Log in with username `admin` and password `MedPass123!`
3. If login succeeds, the CSRF attack bypassed the Referer check

### Reset the password (optional)

1. Go to `http://localhost:4280/vulnerabilities/csrf/`
2. Type `password` in both fields and click `Change`
