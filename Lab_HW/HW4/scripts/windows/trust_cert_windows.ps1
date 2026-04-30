param(
    [string]$CertFile = "certs\\localhost.crt"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $CertFile)) {
    Write-Host "Certificate file not found: $CertFile"
    Write-Host "Generate it first with:"
    Write-Host "  powershell -ExecutionPolicy Bypass -File .\\scripts\\windows\\generate_cert_windows.ps1"
    exit 1
}

Write-Host "This step requires Administrator PowerShell."
Write-Host "Adding certificate to Local Machine Root trust store..."

certutil -addstore -f "Root" "$CertFile"

Write-Host "Done. Certificate trusted by Windows."
