# Step 07: Cleanup

## Stop Lab

Linux:

```bash
cd "/home/mmswflow/Documents/uni-labs/Sem II/security-encryption-labs/HW/HW_1/dvwa-csrf-lab"
docker compose down
```

Windows (PowerShell):

```powershell
Set-Location "C:\path\to\security-encryption-labs\HW\HW_1\dvwa-csrf-lab"
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
