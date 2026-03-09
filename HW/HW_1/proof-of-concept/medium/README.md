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

### Test A: Open from `file://` (often fails)

1. In DVWA, set security level to `medium`
2. Stay logged in
3. Open `proof-of-concept/medium/csrf_poc_medium.html` in the browser
   (use your file manager or browser's open-file dialog to navigate to the repo)
4. Check DVWA response

Expected: usually `That request didn't look correct.` because the browser sends no `Referer` from a local file.

### Test B: Serve from localhost (can pass weak checks)

Start a local static server in the lab folder:

Linux:
```bash
python3 -m http.server 8082
```

Windows (PowerShell):
```powershell
py -m http.server 8082
```

Open in browser:
`http://localhost:8082/proof-of-concept/medium/csrf_poc_medium.html`

Expected: in many setups this passes the weak `Referer` check and the password changes.

## Verify

If password changed, logout and login with `MedPass123!`.
