# Medium Level PoC

## Security Level Behavior

The server checks whether the `Referer` header contains the server name.
This is a weak control: no cryptographic token is used, and the check can be bypassed by serving the PoC from a same-host origin.

## Files

- `csrf_poc_medium.html`
  Same forged GET request as low level.
  Behavior depends on how and where the file is opened.

## Expected Results

**Test A — open from `file://`**
Usually fails with `That request didn't look correct.` because the browser sends no `Referer` from a local file.

**Test B — serve from localhost**
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

In many setups this passes the weak `Referer` check and the password changes.

## Verify

If password changed, logout and login with `MedPass123!`.
