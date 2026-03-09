# Step 04: Medium Level Test

## Goal

Run medium-level CSRF checks and see effect of `Referer` validation.

## Test A: Open PoC from `file://` (often fails)

1. In DVWA, set security level to `medium`
2. Stay logged in
3. Open `proof-of-concept/medium/csrf_poc_medium.html` in the browser
   (use your file manager or browser's open-file dialog to navigate to the repo)

4. Check DVWA response

Expected for Test A:
- Usually `That request didn't look correct.` because `Referer` may be absent.

## Test B: Serve PoC from localhost (can pass weak checks)

1. Open terminal in lab folder
2. Start local static server:

Linux:

```bash
python3 -m http.server 8082
```

Windows (PowerShell):

```powershell
py -m http.server 8082
```

3. In browser, open:

`http://localhost:8082/proof-of-concept/medium/csrf_poc_medium.html`

4. Check DVWA response

Expected for Test B:
- In many setups, weak `Referer` validation is bypassed and password changes.

## Verify

If password changed, logout and login using password from medium PoC file (`MedPass123!`).
