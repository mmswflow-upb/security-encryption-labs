# Step 01: Prerequisites and Start

## Goal

Start DVWA with Docker Compose and confirm it is running.

## Requirements

- Docker installed and running
- Docker Compose v2 available as `docker compose`
- Git with submodule support

## Commands

Run from the repo root.

If you cloned without `--recurse-submodules`, initialize the DVWA source submodule first:

```bash
git submodule update --init
```

Linux (bash):

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
ss -ltnp

# Build from dvwa-source/ and start
docker compose up -d --build

# Verify
docker compose ps
docker compose logs -f --tail=100
```

Windows (PowerShell):

```powershell
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
netstat -ano | findstr LISTENING

docker compose up -d
docker compose ps
docker compose logs -f --tail=100
```

## Expected Result

- Container `dvwa-csrf-lab` is `Up`
- Port mapping includes `8081->80`
- DVWA loads at `http://localhost:8081`
