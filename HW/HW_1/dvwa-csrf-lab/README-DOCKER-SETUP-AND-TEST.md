# Docker Setup and Lab Operations

## What This README Is For

This file covers environment operations:
- port checks
- container start and status checks
- database setup and reset
- stop and cleanup commands

For level-by-level manual testing, use:
- `walkthrough/README-WALKTHROUGH.md`

## Prerequisites

- Docker running
- Docker Compose v2 command available as `docker compose`

## 1) Check Port Conflicts

Linux (bash):

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
ss -ltnp
lsof -i -P -n | grep LISTEN
```

Windows (PowerShell):

```powershell
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
netstat -ano | findstr LISTENING
Get-NetTCPConnection -State Listen | Select-Object LocalAddress,LocalPort,OwningProcess
```

Preferred port order for this lab:
`8080, 8081, 8082, 8083, 8000, 8001, 8888, 5000`

Current lab mapping in `compose.yml`:
- host `8081` -> container `80`

## 2) Start and Verify

From lab folder on Linux:

```bash
cd "/home/mmswflow/Documents/uni-labs/Sem II/security-encryption-labs/HW/HW_1/dvwa-csrf-lab"
docker compose up -d
docker compose ps
docker compose logs -f --tail=100
```

From lab folder on Windows (PowerShell):

```powershell
Set-Location "C:\path\to\security-encryption-labs\HW\HW_1\dvwa-csrf-lab"
docker compose up -d
docker compose ps
docker compose logs -f --tail=100
```

Open:
- `http://localhost:8081`

## 3) Initialize Database (Required)

Important:
- container startup does not automatically run `setup.php`
- you must trigger setup manually

Manual steps:
1. open `http://localhost:8081/setup.php`
2. click `Create / Reset Database`
3. login at `http://localhost:8081/login.php` with `admin / password`

## 4) Quick Health Checks

- web reachable at `http://localhost:8081`
- login works with expected account after setup
- `docker compose ps` shows container status `Up`

## 5) Cleanup

Stop and remove container and network:

Linux:

```bash
docker compose down
```

Windows (PowerShell):

```powershell
docker compose down
```

Full reset including volumes:

Linux:

```bash
docker compose down -v
```

Windows (PowerShell):

```powershell
docker compose down -v
```

Difference:
- `down`: keeps volumes
- `down -v`: removes volumes
