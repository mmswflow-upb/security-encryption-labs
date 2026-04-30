# HW4 - Local SSL Certificate + Flask HTTPS

This homework shows:
1. how to create a local self-signed SSL certificate,
2. how to run Flask over HTTPS with that certificate,
3. how to trust it in your OS trust store.

## Quick Meaning

- SSL certificate: enables encrypted HTTPS.
- Self-signed certificate: created by you locally.
- Trust store: OS/browser list of trusted certificates.

If not trusted, browser shows a certificate warning.

## Script Layout

- Linux scripts:
  - `scripts/linux/generate_cert.sh`
  - `scripts/linux/trust_cert_linux.sh`
  - `scripts/linux/untrust_cert_linux.sh`
- Windows scripts:
  - `scripts/windows/generate_cert_windows.ps1`
  - `scripts/windows/trust_cert_windows.ps1`
  - `scripts/windows/untrust_cert_windows.ps1`

## OS Guides

- Linux guide: `docs/README-linux.md`
- Windows guide: `docs/README-windows.md`
- Detailed explanation: `docs/EXPLANATION.md`

## App Files

- `main.py` - Flask HTTPS app.
- `Dockerfile`, `docker-compose.yml` - containerized run (same style as previous HWs).

## Quick Start (Any OS)

After following your OS guide:

```bash
docker compose up -d --build
```

Open:
- <https://localhost:5000>

Stop:

```bash
docker compose down
```
