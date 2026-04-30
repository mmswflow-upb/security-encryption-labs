#!/usr/bin/env bash
set -euo pipefail

# Removes the local Root CA from the system trust store and from NSS.
# Also cleans up any legacy "hw4-localhost" entries left over from the
# old single-cert flow, so re-running this script is fully idempotent.

CERT_FILE="${1:-certs/rootCA.crt}"
NSS_DB="${HOME}/.pki/nssdb"

# (target_name, nickname) pairs to remove.
# First entry is the current one; the rest are legacy names we may have left behind.
declare -a TARGETS=(
  "hw4-rootCA.crt:hw4-rootCA"
  "hw4-localhost.crt:hw4-localhost"
)

if ! command -v update-ca-certificates >/dev/null 2>&1; then
  echo "update-ca-certificates is not available on this system."
  exit 1
fi

if ! command -v certutil >/dev/null 2>&1; then
  echo "certutil is required to remove the Brave/NSS trust entry but was not found."
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
removed_any=0
for entry in "${TARGETS[@]}"; do
  target_name="${entry%%:*}"
  target_path="/usr/local/share/ca-certificates/${target_name}"
  if [ -f "${target_path}" ]; then
    sudo rm -f "${target_path}"
    removed_any=1
    echo "System trust: removed ${target_path}"
  fi
done
if [ "${removed_any}" -eq 1 ]; then
  sudo update-ca-certificates --fresh >/dev/null
fi

# Sweep /etc/ssl/certs for any leftover hw4-* symlinks.
if find /etc/ssl/certs -maxdepth 1 -name "hw4-*" 2>/dev/null | grep -q .; then
  echo "System trust: removing leftover /etc/ssl/certs/hw4-* symlinks."
  sudo find /etc/ssl/certs -maxdepth 1 -name "hw4-*" -delete
fi

# 2. NSS DB.
if [ ! -f "${NSS_DB}/cert9.db" ] && [ ! -f "${NSS_DB}/cert8.db" ]; then
  echo "NSS trust:    no NSS DB at ${NSS_DB}, skipped."
  exit 0
fi

# 2a. Remove all entries matching any known nickname (with a safety valve).
for entry in "${TARGETS[@]}"; do
  nick="${entry##*:}"
  removed=0
  while certutil -d "sql:${NSS_DB}" -L -n "${nick}" >/dev/null 2>&1; do
    certutil -d "sql:${NSS_DB}" -D -n "${nick}"
    removed=$((removed + 1))
    if [ "${removed}" -gt 10 ]; then
      echo "NSS trust:    aborting after 10 removals of ${nick}; inspect DB manually."
      exit 1
    fi
  done
  if [ "${removed}" -gt 0 ]; then
    echo "NSS trust:    removed ${removed} entry/entries with nickname ${nick}"
  fi
done

# 2b. Defense in depth: remove any other NSS entry whose SHA-256 fingerprint
# matches the local Root CA. Catches manual imports under a different name.
if [ -f "${CERT_FILE}" ]; then
  target_fp=$(openssl x509 -in "${CERT_FILE}" -noout -fingerprint -sha256 \
              | sed 's/^.*=//; s/://g' | tr 'A-F' 'a-f')

  while IFS= read -r nick; do
    [ -z "${nick}" ] && continue
    fp=$(certutil -d "sql:${NSS_DB}" -L -n "${nick}" 2>/dev/null \
         | grep -i "Fingerprint (SHA-256)" -A1 | tail -n1 \
         | tr -d ' :' | tr 'A-F' 'a-f')
    if [ "${fp}" = "${target_fp}" ]; then
      certutil -d "sql:${NSS_DB}" -D -n "${nick}"
      echo "NSS trust:    removed extra entry by fingerprint match: ${nick}"
    fi
  done < <(certutil -d "sql:${NSS_DB}" -L \
           | awk 'NR>4 && NF>=2 {sub(/[[:space:]]+[A-Za-z,]+[[:space:]]*$/,""); print}')
fi

# 3. Verify nothing matching our nicknames remains.
for entry in "${TARGETS[@]}"; do
  nick="${entry##*:}"
  if certutil -d "sql:${NSS_DB}" -L -n "${nick}" >/dev/null 2>&1; then
    echo "NSS trust:    FAILED - ${nick} still present in ${NSS_DB}"
    exit 1
  fi
done
echo "NSS trust:    verified all hw4 entries gone from ${NSS_DB}"

echo
echo "Done. Restart Brave fully (pkill -f brave) and reload https://localhost:5000"
echo "to confirm the warning page returns."
