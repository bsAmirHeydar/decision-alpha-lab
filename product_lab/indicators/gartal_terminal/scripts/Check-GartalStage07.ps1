$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$required = @(
  "mql5\GartalTerminal.mq5",
  "mql5\include\GartalNewsAlerts.mqh",
  "mql5\include\GartalNewsTypes.mqh",
  "mql5\include\GartalNewsInputs.mqh",
  "mql5\include\GartalNewsDiagnostics.mqh",
  "mql5\include\GartalNewsFilters.mqh",
  "mql5\include\GartalNewsDashboard.mqh",
  "spec\STAGE_07_ALERT_ENGINE_STATE_MACHINE.md",
  "obsidian\implementation\stage_07_alert_engine_state_machine.md",
  "obsidian\implementation\stage_07\00_STAGE_07_INDEX.md",
  "obsidian\gartal_terminal_stage_07.canvas"
)

$missing = @()
foreach ($rel in $required) {
  $path = Join-Path $root $rel
  if (!(Test-Path $path)) { $missing += $rel }
}

if ($missing.Count -gt 0) {
  Write-Host "Stage 07 check failed. Missing files:" -ForegroundColor Red
  $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
  exit 1
}

$alerts = Get-Content (Join-Path $root "mql5\include\GartalNewsAlerts.mqh") -Raw
$tokens = @(
  "GT_ProcessAlerts",
  "GT_TrySendAlert",
  "GT_ALERT_STAGE_PRE_30M",
  "GT_ALERT_STAGE_RELEASE",
  "GT_ALERT_STAGE_ACTUAL",
  "GT_ALERT_STAGE_BREAKING",
  "GT_AlertAlreadySent",
  "GT_AlertCooldownPassed"
)

foreach ($token in $tokens) {
  if ($alerts -notmatch [Regex]::Escape($token)) {
    Write-Host "Stage 07 check failed. Token missing: $token" -ForegroundColor Red
    exit 1
  }
}

Write-Host "Stage 07 structural check passed." -ForegroundColor Green
Write-Host "Next: compile product_lab\indicators\gartal_terminal\mql5\GartalTerminal.mq5 in MetaEditor." -ForegroundColor Cyan
