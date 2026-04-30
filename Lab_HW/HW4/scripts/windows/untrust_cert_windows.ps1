param(
    [string]$CertFile = "certs\\localhost.crt"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $CertFile)) {
    Write-Host "Certificate file not found: $CertFile"
    Write-Host "Cannot compute thumbprint for removal."
    exit 1
}

$cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($CertFile)
$thumbprint = $cert.Thumbprint

Write-Host "This step requires Administrator PowerShell."
Write-Host "Removing certificate thumbprint from Local Machine Root store:"
Write-Host "  $thumbprint"

certutil -delstore "Root" "$thumbprint"

Write-Host "Done. Certificate removal command executed."
