$ErrorActionPreference = "Stop"

$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-saed-v4-25-continual-meta-transfer-v1.0.0*.zip" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) {
    throw "SAED V4-25 ZIP patch was not found in the repository root."
}

Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
