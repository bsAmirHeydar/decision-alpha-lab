param(
  [string]$Version = "1.0.0-beta",
  [switch]$WithSource
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Required = @(
  "mql5\GartalTerminal.mq5",
  "mql5\include\GartalNewsProduct.mqh",
  "mql5\experts\GartalNewsDownloaderEA.mq5",
  "mql5\presets\gartal_terminal_live_bridge.set",
  "release\customer_docs\INSTALL_CUSTOMER_EN.md",
  "release\customer_docs\INSTALL_CUSTOMER_FA.md",
  "release\customer_docs\BETA_QA_CHECKLIST.md"
)

$missing = @()
foreach ($r in $Required) {
  $path = Join-Path $Root $r
  if (!(Test-Path $path)) { $missing += $r }
}

if ($missing.Count -gt 0) {
  Write-Host "Missing release files:" -ForegroundColor Red
  $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
  exit 1
}

& (Join-Path $PSScriptRoot "Package-GartalTerminal.ps1") -Version $Version -Channel beta -IncludeSource:$WithSource
