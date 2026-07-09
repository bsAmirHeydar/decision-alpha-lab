$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$required = @(
  "mql5/GartalTerminal.mq5",
  "mql5/include/GartalNewsFilters.mqh",
  "mql5/include/GartalNewsDashboard.mqh",
  "mql5/include/GartalNewsDashboardTheme.mqh",
  "mql5/include/GartalNewsInputs.mqh",
  "mql5/include/GartalNewsTypes.mqh",
  "mql5/include/GartalNewsDiagnostics.mqh",
  "spec/STAGE_06_RUNTIME_FILTER_ENGINE.md",
  "obsidian/implementation/stage_06_runtime_filter_engine.md",
  "obsidian/implementation/stage_06/00_STAGE_06_INDEX.md",
  "obsidian/gartal_terminal_stage_06.canvas"
)

$missing = @()
foreach ($file in $required) {
  $path = Join-Path $root $file
  if (!(Test-Path $path)) { $missing += $file }
}

if ($missing.Count -gt 0) {
  Write-Host "Stage 06 check failed. Missing files:" -ForegroundColor Red
  $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
  exit 1
}

$mq5 = Get-Content (Join-Path $root "mql5/GartalTerminal.mq5") -Raw
if ($mq5 -notmatch "GartalNewsFilters.mqh") {
  Write-Host "Stage 06 check failed: GartalNewsFilters.mqh is not included." -ForegroundColor Red
  exit 1
}

$filters = Get-Content (Join-Path $root "mql5/include/GartalNewsFilters.mqh") -Raw
foreach ($token in @("GT_HandleRuntimeFilterClick", "GT_ToggleCsvItem", "GT_FilterSummary")) {
  if ($filters -notmatch $token) {
    Write-Host "Stage 06 check failed: missing $token." -ForegroundColor Red
    exit 1
  }
}

Write-Host "Stage 06 runtime filter engine file check passed." -ForegroundColor Green
