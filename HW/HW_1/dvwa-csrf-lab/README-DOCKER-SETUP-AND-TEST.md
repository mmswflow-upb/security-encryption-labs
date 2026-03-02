# Docker Setup, Run, and Multi-Level Testing

## Goal

Run **Damn Vulnerable Web Application (DVWA)** locally with Docker Compose and test **Cross-Site Request Forgery (CSRF)** behavior across all security levels.

## Prerequisites

- Docker installed and running
- Docker Compose v2 available as `docker compose`
- Local shell access

## 1) Check Port Conflicts Before Start

Run:

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
ss -ltnp
lsof -i -P -n | grep LISTEN
```

Choose first free port in this order:
`8080, 8081, 8082, 8083, 8000, 8001, 8888, 5000`

This lab currently maps:
- host `8081` to container `80`

## 2) Start and Verify

From `dvwa-csrf-lab/`:

```bash
docker compose up -d
docker compose ps
docker compose logs -f --tail=100
```

Open:
- `http://localhost:8081`

## 3) Initialize DVWA

1. Login with default credentials:
- username: `admin`
- password: `password`
2. Open `DVWA Security`.
3. Set security level and click `Submit`.
4. Open `Database Setup` (`/setup.php`).
5. Click `Create / Reset Database`.

## 4) Run CSRF Tests by Level

### Low Level

1. Set security to `low`.
2. Open:
- `file:///home/mmswflow/Documents/uni-labs/Sem%20II/security-encryption-labs/HW/HW_1/dvwa-csrf-lab/csrf_poc.html`
3. Expected: password changes.

### Medium Level

1. Set security to `medium`.
2. First try:
- `file:///home/mmswflow/Documents/uni-labs/Sem%20II/security-encryption-labs/HW/HW_1/dvwa-csrf-lab/csrf_poc_medium.html`
3. If this fails due missing `Referer`, serve the folder on localhost:

```bash
cd "/home/mmswflow/Documents/uni-labs/Sem II/security-encryption-labs/HW/HW_1/dvwa-csrf-lab"
python3 -m http.server 8082
```

4. Then open:
- `http://localhost:8082/csrf_poc_medium.html`
5. Expected: in many setups, weak `Referer` checks can be bypassed.

### High Level

1. Set security to `high`.
2. Open expected-fail file:
- `csrf_poc_high_missing_token.html`
3. Expected: fail because `user_token` is missing.
4. Optional controlled test:
- open DVWA CSRF page and copy `user_token`
- insert into `csrf_poc_high_manual_token.html`
- open that file
5. Expected: request can succeed only with valid token from active session.

### Impossible Level

1. Set security to `impossible`.
2. Open expected-fail file:
- `csrf_poc_impossible_missing_requirements.html`
3. Expected: fail.
4. Optional controlled test:
- copy `user_token` from form
- provide current password in `csrf_poc_impossible_manual_token.html`
- open file
5. Expected: success only when both token and current password are correct.

## 5) Verify Outcome Safely

After each attempt:

1. Sign out.
2. Try signing in with original password.
3. Try signing in with test password used in PoC.
4. Record result per level.

## 6) Cleanup

```bash
docker compose down
```

Use this for full reset including volumes:

```bash
docker compose down -v
```

Difference:
- `down` keeps volumes
- `down -v` removes volumes

## 7) Lab Safety Reminder

- Keep testing on localhost only.
- Do not test on real targets without explicit written authorization.
