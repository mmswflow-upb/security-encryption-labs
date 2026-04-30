#!/usr/bin/env bash
set -euo pipefail

# Generates a local CA + leaf cert pair (mkcert-style).
#
# Why two certs and not one self-signed cert?
# Chromium-based browsers (Brave/Chrome/Edge) reject a single self-signed
# certificate that acts as both the TLS leaf AND its own trust anchor with
# NET::ERR_CERT_INVALID. The chain builder requires a real chain:
# leaf -> root, where the leaf is CA:FALSE and the root is CA:TRUE.
# We therefore generate:
#   - rootCA.crt     : CA:TRUE, no serverAuth EKU, long-lived. Trusted in OS/NSS.
#   - localhost.crt  : CA:FALSE, serverAuth, SAN=localhost+127.0.0.1, signed by rootCA.

CERT_DIR="certs"
ROOT_KEY="${CERT_DIR}/rootCA.key"
ROOT_CRT="${CERT_DIR}/rootCA.crt"
LEAF_KEY="${CERT_DIR}/localhost.key"
LEAF_CRT="${CERT_DIR}/localhost.crt"
LEAF_CSR="${CERT_DIR}/localhost.csr"
ROOT_SRL="${CERT_DIR}/rootCA.srl"

mkdir -p "${CERT_DIR}"

# 1. Root CA - self-signed, CA:TRUE, NO serverAuth EKU.
openssl req -x509 -nodes -newkey rsa:2048 -sha256 -days 3650 \
  -keyout "${ROOT_KEY}" \
  -out "${ROOT_CRT}" \
  -subj "/C=RO/ST=Bucharest/L=Bucharest/O=UniLabs/OU=HW4/CN=HW4 Local Dev Root" \
  -addext "basicConstraints=critical,CA:TRUE,pathlen:0" \
  -addext "keyUsage=critical,keyCertSign,cRLSign"

# 2. Leaf key + CSR.
openssl req -nodes -newkey rsa:2048 -sha256 \
  -keyout "${LEAF_KEY}" \
  -out "${LEAF_CSR}" \
  -subj "/C=RO/ST=Bucharest/L=Bucharest/O=UniLabs/OU=HW4/CN=localhost"

# 3. Sign the leaf with the root CA, embedding SAN/EKU/KU/BasicConstraints.
LEAF_EXT_FILE="$(mktemp)"
trap 'rm -f "${LEAF_EXT_FILE}" "${LEAF_CSR}" "${ROOT_SRL}"' EXIT
cat > "${LEAF_EXT_FILE}" <<'EOF'
basicConstraints=critical,CA:FALSE
subjectAltName=DNS:localhost,IP:127.0.0.1
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
EOF

openssl x509 -req -in "${LEAF_CSR}" -days 825 -sha256 \
  -CA "${ROOT_CRT}" -CAkey "${ROOT_KEY}" -CAcreateserial \
  -extfile "${LEAF_EXT_FILE}" \
  -out "${LEAF_CRT}"

chmod 600 "${ROOT_KEY}" "${LEAF_KEY}"

echo
echo "Created:"
echo "  Root CA cert : ${ROOT_CRT}   (trust this in OS + NSS)"
echo "  Root CA key  : ${ROOT_KEY}   (private; keep local)"
echo "  Server leaf  : ${LEAF_CRT}   (served by Flask)"
echo "  Server key   : ${LEAF_KEY}   (private; keep local)"
