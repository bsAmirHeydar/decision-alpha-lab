$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Required = @(
  "mql5\GartalTerminal.mq5",
  "mql5\include\GartalNewsTypes.mqh",
  "mql5\include\GartalNewsInputs.mqh",
  "mql5\include\GartalNewsDiagnostics.mqh",
  "mql5\include\GartalNewsCalendarClient.mqh",
  "mql5\include\GartalNewsResilience.mqh",
  "mql5\include\GartalNewsParser.mqh",
  "mql5\include\GartalNewsDashboard.mqh",
  "mql5\include\GartalNewsDashboardTheme.mqh",
  "mql5\experts\GartalNewsDownloaderEA.mq5",
  "spec\STAGE_09_CACHE_FALLBACK_RESILIENCE_LAYER.md",
  "obsidian\implementation\stage_09_cache_fallback_resilience_layer.md",
  "obsidian\implementation\stage_09\00_STAGE_09_INDEX.md"
)

$Missing = @()
foreach($Item in $Required) {
  $Path = Join-Path $Root $Item
  if(!(Test-Path $Path)) { $Missing += $Item }
}

if($Missing.Count -gt 0) {
  Write-Host "Stage 09 check FAILED. Missing files:" -ForegroundColor Red
  $Missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
  exit 1
}

$Main = Get-Content (Join-Path $Root "mql5\GartalTerminal.mq5") -Raw
$Tokens = @(
  "GartalNewsResilience.mqh",
  "GT_ResilienceRefreshAllowed",
  "GT_CheckRawCalendarHealth",
  "GT_SaveVerifiedCacheBundle",
  "GT_LoadCacheBundle",
  "GT_ApplySourceQualityToStore"
)
foreach($Token in $Tokens) {
  if($Main -notmatch [regex]::Escape($Token)) {
    Write-Host "Stage 09 check FAILED. Main file missing token: $Token" -ForegroundColor Red
    exit 1
  }
}

$Resilience = Get-Content (Join-Path $Root "mql5\include\GartalNewsResilience.mqh") -Raw
$ResilienceTokens = @(
  "GT_SOURCE_QUALITY_LIVE",
  "GT_CACHE_STATE_STALE",
  "GT_CountToken",
  "GT_MetaGet",
  "GT_ClassifyLoadedCache",
  "GT_ResilienceCompactSummary"
)
foreach($Token in $ResilienceTokens) {
  if($Resilience -notmatch [regex]::Escape($Token)) {
    Write-Host "Stage 09 check FAILED. Resilience module missing token: $Token" -ForegroundColor Red
    exit 1
  }
}

Write-Host "Stage 09 check PASSED: cache/fallback/resilience files and integration tokens are present." -ForegroundColor Green
Write-Host "Next: compile mql5\GartalTerminal.mq5 and mql5\experts\GartalNewsDownloaderEA.mq5 inside MetaEditor."
