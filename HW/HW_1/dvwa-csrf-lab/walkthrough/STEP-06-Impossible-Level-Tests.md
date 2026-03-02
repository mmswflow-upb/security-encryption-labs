# Step 06: Impossible Level Tests

## Goal

Show that impossible level needs both valid token and current password.

## Test A: Missing requirements (should fail)

1. In DVWA, set security level to `impossible`
2. Stay logged in
3. Open:

`file:///home/mmswflow/Documents/uni-labs/Sem%20II/security-encryption-labs/HW/HW_1/dvwa-csrf-lab/csrf_poc_impossible_missing_requirements.html`

Windows example:

`file:///C:/path/to/security-encryption-labs/HW/HW_1/dvwa-csrf-lab/csrf_poc_impossible_missing_requirements.html`

Expected:
- DVWA rejects request because requirements are missing.

## Test B: Manual token + current password (controlled success)

1. Keep security at `impossible`
2. Open `http://localhost:8081/vulnerabilities/csrf/`
3. Copy `user_token` value from form
4. Determine current password for current user (from previous successful step)
5. Edit `csrf_poc_impossible_manual_token.html`
6. Replace:
- `IMPOSSIBLE_TOKEN` with token value
- `CURRENT_PASSWORD` with current real password
7. Open:

`file:///home/mmswflow/Documents/uni-labs/Sem%20II/security-encryption-labs/HW/HW_1/dvwa-csrf-lab/csrf_poc_impossible_manual_token.html`

Windows example:

`file:///C:/path/to/security-encryption-labs/HW/HW_1/dvwa-csrf-lab/csrf_poc_impossible_manual_token.html`

Expected:
- If both values are correct, DVWA can show `Password Changed.`

## Verify

Try login with password from file (`ImpManual123!`).
