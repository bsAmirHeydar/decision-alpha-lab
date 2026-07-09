$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Files = @(
  "mql5/GartalTerminal.mq5",
  "mql5/include/GartalNewsTypes.mqh",
  "mql5/include/GartalNewsUtils.mqh",
  "mql5/include/GartalNewsInputs.mqh",
  "mql5/include/GartalNewsTime.mqh",
  "mql5/include/GartalNewsStore.mqh",
  "mql5/include/GartalNewsSampleData.mqh",
  "mql5/include/GartalNewsDashboard.mqh",
  "mql5/include/GartalNewsTimeline.mqh",
  "spec/STAGE_03_TIME_NORMALIZATION_ENGINE.md",
  "obsidian/implementation/stage_03_broker_gmt_time_normalization.md",
  "obsidian/implementation/stage_03/00_STAGE_03_INDEX.md"
)

Write-Host "gartal terminal Stage 03 structural check" -ForegroundColor Cyan

foreach ($file in $Files) {
  $path = Join-Path $Root $file
  if (!(Test-Path $path)) {
    throw "Missing required Stage 03 file: $file"
  }
  Write-Host "OK  $file" -ForegroundColor Green
}

$TimeFile = Join-Path $Root "mql5/include/GartalNewsTime.mqh"
$TimeText = Get-Content $TimeFile -Raw
$RequiredFunctions = @(
  "GT_NormalizeConfigTime",
  "GT_DetectBrokerGmtOffsetSeconds",
  "GT_SourceToBrokerTime",
  "GT_UtcToBrokerTime",
  "GT_BrokerToUtcTime",
  "GT_ConfiguredSampleBrokerTime",
  "GT_UpdateEventTimeFields"
)

foreach ($fn in $RequiredFunctions) {
  if ($TimeText -notmatch $fn) {
    throw "Missing time engine function: $fn"
  }
  Write-Host "OK  function $fn" -ForegroundColor Green
}

Write-Host "Stage 03 structural check passed. Compile GartalTerminal.mq5 in MetaEditor for final MQL5 validation." -ForegroundColor Cyan
