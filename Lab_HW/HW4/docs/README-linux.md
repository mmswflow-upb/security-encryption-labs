# HW4 Linux Guide (Brave)

This guide is for Linux + Brave (tested on Debian/Ubuntu).
Firefox is intentionally not covered.

## Why a Root CA + leaf cert (and not a single self-signed cert)?

Chromium-based browsers (Brave/Chrome/Edge) reject a single self-signed
certificate that is used as both the TLS leaf AND its own trust anchor:
the chain builder fails with `NET::ERR_CERT_INVALID` because the leaf
and the trust anchor are the same certificate. NSS, curl, and openssl
do not enforce this, so curl looks fine while Brave keeps rejecting.

The fix is the standard mkcert pattern:

- a **Root CA** cert (`certs/rootCA.crt`): `CA:TRUE`, no `serverAuth` EKU,
  long-lived. This is what is imported into the OS / NSS trust store.
- a **leaf** cert (`certs/localhost.crt`): `CA:FALSE`, `serverAuth`,
  `subjectAltName=DNS:localhost,IP:127.0.0.1`, signed by the Root CA.
  Flask serves this leaf.

Brave then builds the chain `localhost` -> `HW4 Local Dev Root` and
validates against the trusted root.

## Why two trust stores?

On Linux, Brave/Chromium does NOT use the system trust store at
`/etc/ssl/certs` for user-imported certs. It reads from the per-user NSS
database at `~/.pki/nssdb`, manipulated via `certutil` from `libnss3-tools`.

Adding the Root CA only with `update-ca-certificates` makes `curl` and
`openssl` happy but Brave keeps showing a warning. Both stores must be
updated; the trust script does both.

## 1. Install prerequisites

```bash
sudo apt install libnss3-tools
```

(The trust/untrust scripts will auto-install this if it is missing.)

## 2. Generate the Root CA + leaf cert pair

```bash
chmod +x scripts/linux/generate_cert.sh scripts/linux/trust_cert_linux.sh scripts/linux/untrust_cert_linux.sh
./scripts/linux/generate_cert.sh
```

Creates:

- `certs/rootCA.crt`    - Root CA (CA:TRUE, no EKU, 10 years)
- `certs/rootCA.key`    - Root CA private key
- `certs/localhost.crt` - leaf signed by Root CA (CA:FALSE, serverAuth, SAN)
- `certs/localhost.key` - leaf private key

Re-running this script regenerates everything.

## 3. Trust the Root CA

```bash
./scripts/linux/trust_cert_linux.sh
```

This imports `certs/rootCA.crt` into:

- `/usr/local/share/ca-certificates/hw4-rootCA.crt` + `update-ca-certificates`
  (system trust, used by curl/openssl)
- `~/.pki/nssdb` with trust flags `C,,` under nickname `hw4-rootCA`
  (NSS trust, used by Brave)

Idempotent: re-running it removes any prior `hw4-rootCA` entry before
re-adding.

## 4. Start Flask HTTPS App with Docker

```bash
docker compose up -d --build
```

Flask serves `certs/localhost.crt` (the leaf) and presents only that cert
in the handshake; the browser pulls the Root CA from NSS.

## 5. Open in Brave

**Fully quit Brave first** (close all windows AND any tray/background processes):

```bash
pkill -f brave; sleep 1
brave-browser https://localhost:5000 &
```

Brave caches cert decisions per running session, so an already-open Brave
will keep showing the old warning page until restarted.

If you previously clicked through the warning, Brave may also have cached
an HSTS-style decision for `localhost`. Clear it via:
`brave://net-internals/#hsts` -> "Delete domain security policies" -> `localhost`.

## 6. Verify

```bash
# Root CA fingerprint (this is what we trusted)
openssl x509 -in certs/rootCA.crt -noout -fingerprint -sha256 -subject -issuer

# Leaf fingerprint and that it is signed by the Root CA
openssl x509 -in certs/localhost.crt -noout -fingerprint -sha256 -subject -issuer

# Verify the leaf chains to the Root CA
openssl verify -CAfile certs/rootCA.crt certs/localhost.crt

# Cert actually served by the container (must match the LEAF fingerprint)
openssl s_client -connect localhost:5000 -servername localhost </dev/null 2>/dev/null \
  | openssl x509 -noout -fingerprint -sha256 -subject -issuer

# NSS trust entry (Root CA)
certutil -d sql:$HOME/.pki/nssdb -L | grep hw4-rootCA
certutil -d sql:$HOME/.pki/nssdb -L -n hw4-rootCA

# System trust (uses /etc/ssl/certs)
curl -v https://localhost:5000 2>&1 | grep -E "(SSL certificate verify|subject:|issuer:)"

# App tests
docker compose run --rm web pytest -q
```

## 7. Stop

```bash
docker compose down
```

## 8. Cleanup (remove trust)

```bash
./scripts/linux/untrust_cert_linux.sh
```

Removes:

- `/usr/local/share/ca-certificates/hw4-rootCA.crt` (and the legacy
  `hw4-localhost.crt` if present) + `update-ca-certificates --fresh`
- NSS nicknames `hw4-rootCA` and `hw4-localhost` from `~/.pki/nssdb`
- any leftover `/etc/ssl/certs/hw4-*` symlinks
- any other NSS entry whose fingerprint matches `certs/rootCA.crt`
  (defense against manual imports under a different name)

The script fails loudly if `certutil` is missing (auto-installs it via apt
when possible) so you cannot end up in a state where the system trust
was removed but the NSS entry silently survived.
