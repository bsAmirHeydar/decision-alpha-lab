param([string]$ZipPath = ".\decision-alpha-lab-saed-v4-26-mechanistic-interpretability-v1.0.0.zip")
$ErrorActionPreference = "Stop"
if (-not (Test-Path -LiteralPath $ZipPath)) { throw "ZIP patch not found: $ZipPath" }
Expand-Archive -LiteralPath $ZipPath -DestinationPath . -Force
Remove-Item -LiteralPath $ZipPath -Force
