# Docker Setup and Lab Operations

## What This README Is For

This file covers environment operations:
- submodule initialization
- port checks
- container start and status checks
- database setup and reset
- stop and cleanup commands

For level-by-level manual testing, use:
- `walkthrough/README-WALKTHROUGH.md`

## Docker Setup

This lab uses the official DVWA compose file located at `dvwa-source/compose.yml`.

- Image: `ghcr.io/digininja/dvwa:latest` (pulled from registry)
- App service: `dvwa` on port `4280`
- Database service: `db` running MariaDB 10 (internal only)

All `docker compose` commands use `-f dvwa-source/compose.yml` to reference the original file.

## Prerequisites

- Docker installed and running
- Docker Compose v2 available as `docker compose`
- Git with submodule support

## 0) Initialize Submodule

If you cloned without `--recurse-submodules`, initialize `dvwa-source/` first:

```bash
git submodule update --init
```

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

Current lab mapping in `dvwa-source/compose.yml`:
- host `4280` -> container `80`

## 2) Start

From the repo root:

```bash
docker compose -f dvwa-source/compose.yml up -d
docker compose -f dvwa-source/compose.yml ps
docker compose -f dvwa-source/compose.yml logs -f --tail=100
```

Open:
- `http://localhost:4280`

## 3) Initialize Database (Required)

Important:
- container startup does not automatically run `setup.php`
- you must trigger setup manually

Manual steps:
1. open `http://localhost:4280/setup.php`
2. click `Create / Reset Database`
3. login at `http://localhost:4280/login.php` with `admin / password`

## 4) Quick Health Checks

- web reachable at `http://localhost:4280`
- login works with expected account after setup
- `docker compose -f dvwa-source/compose.yml ps` shows both `dvwa` and `db` as `Up`

## 5) Cleanup

Stop and remove containers and network:

```bash
docker compose -f dvwa-source/compose.yml down
```

Full reset including volumes (wipes database):

```bash
docker compose -f dvwa-source/compose.yml down -v
```

Difference:
- `down`: keeps volumes (database persists)
- `down -v`: removes volumes (full reset)
