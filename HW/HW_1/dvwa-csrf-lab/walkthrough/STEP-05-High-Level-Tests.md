# Step 05: High Level Tests

## Goal

Show difference between missing token and valid token at high level.

## Test A: Missing token (should fail)

1. In DVWA, set security level to `high`
2. Stay logged in
3. Open:

`file:///home/mmswflow/Documents/uni-labs/Sem%20II/security-encryption-labs/HW/HW_1/dvwa-csrf-lab/csrf_poc_high_missing_token.html`

Expected:
- Request fails, typically with token error.

## Test B: Manual valid token (controlled success)

1. Keep security at `high`
2. Open `http://localhost:8081/vulnerabilities/csrf/`
3. Inspect form and copy `user_token` value
4. Edit file `csrf_poc_high_manual_token.html`
5. Replace `HIGH_TOKEN` with copied token
6. Open file:

`file:///home/mmswflow/Documents/uni-labs/Sem%20II/security-encryption-labs/HW/HW_1/dvwa-csrf-lab/csrf_poc_high_manual_token.html`

Expected:
- With valid active-session token, DVWA can show `Password Changed.`

## Verify

Try login with password used in file (`HighManual123!`).
