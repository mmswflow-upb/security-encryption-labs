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

Start:

```bash
docker compose -f dvwa-source/compose.yml up -d
docker compose -f dvwa-source/compose.yml ps
docker compose -f dvwa-source/compose.yml logs -f --tail=100
```

## Expected Result

- Both `dvwa` and `db` services are `Up`
- Port mapping includes `4280->80`
- DVWA loads at `http://localhost:4280`
