# Step 01: Prerequisites and Start

## Goal

Start DVWA with Docker Compose and confirm it is running.

## Requirements

- Docker installed and running
- Docker Compose v2 available as `docker compose`

## Commands

Linux (bash):

```bash
cd "/home/mmswflow/Documents/uni-labs/Sem II/security-encryption-labs/HW/HW_1/dvwa-csrf-lab"

docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
ss -ltnp

# Start DVWA
docker compose up -d

# Verify
docker compose ps
docker compose logs -f --tail=100
```

Windows (PowerShell):

```powershell
Set-Location "C:\path\to\security-encryption-labs\HW\HW_1\dvwa-csrf-lab"

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
