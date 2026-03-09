# Step 07: Cleanup

## Stop Lab

Run from the repo root:

```bash
docker compose down
```

This stops and removes the container and network, but keeps volumes.

## Full Reset

Linux:

```bash
docker compose down -v
```

Windows (PowerShell):

```powershell
docker compose down -v
```

This also removes volumes and resets persisted data.
