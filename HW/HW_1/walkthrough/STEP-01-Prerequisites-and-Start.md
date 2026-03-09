# Step 01: Prerequisites and Start

## Goal

Start DVWA with Docker Compose and confirm it is running.

For full setup options (port conflict checks, health checks), see [docs/README-DOCKER-SETUP-AND-TEST.md](../docs/README-DOCKER-SETUP-AND-TEST.md).

## Commands

Run from the repo root.

If you cloned without `--recurse-submodules`, initialize the DVWA source submodule first:

```bash
git submodule update --init
```

Build and start:

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f --tail=100
```

## Expected Result

- Container `dvwa-csrf-lab` is `Up`
- Port mapping includes `8081->80`
- DVWA loads at `http://localhost:8081`
