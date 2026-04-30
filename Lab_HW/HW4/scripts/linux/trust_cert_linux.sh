#!/usr/bin/env bash
set -euo pipefail

# Trusts the local Root CA (certs/rootCA.crt) in:
#   - the system trust store (used by curl/openssl)
#   - the per-user NSS database (used by Brave/Chromium on Linux)
#
# We trust the ROOT, not the leaf. The Flask server still serves the leaf
# (certs/localhost.crt). Brave then builds the chain leaf -> root and validates.

CERT_FILE="${1:-certs/rootCA.crt}"
TARGET_NAME="hw4-rootCA.crt"
TARGET_PATH="/usr/local/share/ca-certificates/${TARGET_NAME}"
NSS_DB="${HOME}/.pki/nssdb"
NSS_NICKNAME="hw4-rootCA"

if [ ! -f "${CERT_FILE}" ]; then
  echo "Root CA file not found: ${CERT_FILE}"
  echo "Generate it first with: ./scripts/linux/generate_cert.sh"
  exit 1
fi

if ! command -v update-ca-certificates >/dev/null 2>&1; then
  echo "update-ca-certificates is not available on this system."
  echo "Use your OS certificate tool to import: ${CERT_FILE}"
  exit 1
fi

# certutil (libnss3-tools) is REQUIRED on Linux: Brave/Chromium read trust
# from ~/.pki/nssdb, NOT /usr/local/share/ca-certificates.
if ! command -v certutil >/dev/null 2>&1; then
  echo "certutil is required for Brave/Chromium trust but was not found."
  if command -v apt-get >/dev/null 2>&1; then
    echo "Installing libnss3-tools via apt..."
    sudo apt-get update -qq
    sudo apt-get install -y libnss3-tools
  else
    echo "Install it manually (Debian/Ubuntu): sudo apt install libnss3-tools"
    echo "Then re-run this script."
    exit 1
  fi
fi

# 1. System trust store.
sudo cp "${CERT_FILE}" "${TARGET_PATH}"
sudo update-ca-certificates
echo "System trust: installed ${TARGET_PATH}"

# 2. NSS DB (Brave/Chromium).
mkdir -p "${NSS_DB}"
if [ ! -f "${NSS_DB}/cert9.db" ] && [ ! -f "${NSS_DB}/cert8.db" ]; then
  certutil -d "sql:${NSS_DB}" -N --empty-password
fi

# Idempotent: drop any prior entry under the same nickname, then add.
certutil -d "sql:${NSS_DB}" -D -n "${NSS_NICKNAME}" >/dev/null 2>&1 || true
certutil -d "sql:${NSS_DB}" -A -t "C,," -n "${NSS_NICKNAME}" -i "${CERT_FILE}"
echo "NSS trust:    imported ${NSS_NICKNAME} into ${NSS_DB} with flags C,,"

echo
echo "Verify (should show ${NSS_NICKNAME} with trust flags 'C,,'):"
certutil -d "sql:${NSS_DB}" -L | grep "${NSS_NICKNAME}" || true

echo
echo "Done. Now FULLY quit Brave (close all windows AND background processes)"
echo "before reopening https://localhost:5000:"
echo "    pkill -f brave; sleep 1; brave-browser https://localhost:5000 &"
