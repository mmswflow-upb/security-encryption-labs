param(
    [string]$CertDir = "certs"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command openssl -ErrorAction SilentlyContinue)) {
    Write-Host "OpenSSL is required on Windows for this script."
    Write-Host "Install Git for Windows (includes openssl) or OpenSSL, then retry."
    exit 1
}

New-Item -ItemType Directory -Force -Path $CertDir | Out-Null

$certFile = Join-Path $CertDir "localhost.crt"
$keyFile = Join-Path $CertDir "localhost.key"

openssl req -x509 -nodes -newkey rsa:2048 -sha256 -days 825 `
  -keyout "$keyFile" `
  -out "$certFile" `
  -subj "/C=RO/ST=Bucharest/L=Bucharest/O=UniLabs/OU=HW4/CN=localhost" `
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1" `
  -addext "keyUsage=digitalSignature,keyEncipherment" `
  -addext "extendedKeyUsage=serverAuth"

Write-Host "Certificate created:"
Write-Host "  $certFile"
Write-Host "  $keyFile"
