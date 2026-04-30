# HW4 Windows Guide

This guide is for Windows (PowerShell + Docker Desktop).

## 1. Generate Local SSL Certificate

Run from project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows\generate_cert_windows.ps1
```

This creates:
- `certs\localhost.crt`
- `certs\localhost.key`

## 2. Trust the Certificate (Windows trust store)

Open PowerShell as **Administrator**, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows\trust_cert_windows.ps1
```

This runs:
- `certutil -addstore -f Root certs\localhost.crt`

## 3. Start Flask HTTPS App with Docker

```powershell
docker compose up -d --build
```

Open:
- <https://localhost:5000>

## 4. Verify

```powershell
docker compose run --rm web pytest -q
curl.exe -vk https://localhost:5000
```

## 5. Stop

```powershell
docker compose down
```

## 6. Optional Cleanup (Remove from Trust Store)

Open PowerShell as **Administrator**, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows\untrust_cert_windows.ps1
```
