$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Required = @(
  "mql5\GartalTerminal.mq5",
  "mql5\include\GartalNewsProduct.mqh",
  "mql5\include\GartalNewsInputs.mqh",
  "mql5\include\GartalNewsTypes.mqh",
  "mql5\include\GartalNewsDashboard.mqh",
  "mql5\presets\gartal_terminal_beta_sample.set",
  "mql5\presets\gartal_terminal_live_bridge.set",
  "mql5\presets\gartal_terminal_stable_customer.set",
  "release\customer_docs\INSTALL_CUSTOMER_EN.md",
  "release\customer_docs\INSTALL_CUSTOMER_FA.md",
  "release\customer_docs\BETA_QA_CHECKLIST.md",
  "release\customer_docs\RELEASE_MANIFEST_TEMPLATE.md",
  "spec\STAGE_10_PRODUCT_HARDENING_PACKAGING_RELEASE_BUILD.md",
  "obsidian\implementation\stage_10_product_hardening_packaging_release_build.md"
)

$missing = @()
foreach ($r in $Required) {
  $path = Join-Path $Root $r
  if (!(Test-Path $path)) { $missing += $r }
}

if ($missing.Count -gt 0) {
  Write-Host "Stage 10 check failed. Missing files:" -ForegroundColor Red
  $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
  exit 1
}

$mq5 = Get-Content (Join-Path $Root "mql5\GartalTerminal.mq5") -Raw
foreach ($needle in @("GartalNewsProduct.mqh", "GT_ApplyReleaseProfile", "GT_ProductValidateLicense")) {
  if ($mq5 -notmatch [regex]::Escape($needle)) { throw "Missing MQL5 integration marker: $needle" }
}

Write-Host "Stage 10 structure check passed." -ForegroundColor Green
