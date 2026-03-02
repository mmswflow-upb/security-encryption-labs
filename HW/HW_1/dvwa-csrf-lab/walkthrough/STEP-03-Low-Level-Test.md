# Step 03: Low Level Test

## Goal

Demonstrate a successful CSRF password change on low level.

## Manual Steps

1. In DVWA, open `DVWA Security`
2. Set level to `low` and click `Submit`
3. Ensure you are still logged in as `admin`
4. Open this file in browser:

`file:///home/mmswflow/Documents/uni-labs/Sem%20II/security-encryption-labs/HW/HW_1/dvwa-csrf-lab/csrf_poc.html`

Windows example:

`file:///C:/path/to/security-encryption-labs/HW/HW_1/dvwa-csrf-lab/csrf_poc.html`

5. Return to DVWA and observe the message on CSRF page
6. Logout and login again with:
- username: `admin`
- password: `NewPass123!`

## Expected Result

- DVWA shows `Password Changed.`
- Login with `NewPass123!` succeeds
