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

This lab builds DVWA from source using the official Dockerfile in the `dvwa-source/` submodule.

- Build context: `./dvwa-source` (the submodule)
- App service: `dvwa-csrf-lab` on port `8081`
- Database service: `dvwa-csrf-lab-db` running MariaDB 10 (internal only)

The `compose.yml` sets `pull_policy: build`, so Docker always builds the image from the local source instead of pulling a pre-built image.

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

Preferred port order for this lab:
`8080, 8081, 8082, 8083, 8000, 8001, 8888, 5000`

Current lab mapping in `compose.yml`:
- host `8081` -> container `80`

## 2) Build and Start

From the repo root:

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f --tail=100
```

The `--build` flag ensures the image is built from `dvwa-source/` before starting.

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
- `docker compose ps` shows both `dvwa-csrf-lab` and `dvwa-csrf-lab-db` as `Up`

## 5) Cleanup

Stop and remove containers and network:

```bash
docker compose down
```

Full reset including volumes (wipes database):

```bash
docker compose down -v
```

Difference:
- `down`: keeps volumes (database persists)
- `down -v`: removes volumes (full reset)
