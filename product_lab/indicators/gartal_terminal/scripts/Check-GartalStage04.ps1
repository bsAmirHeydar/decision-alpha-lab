$ErrorActionPreference = "Stop"

$required = @(
  "product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsChartGeometry.mqh",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsTimeline.mqh",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsInputs.mqh",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsTypes.mqh",
  "product_lab/indicators/gartal_terminal/spec/STAGE_04_CHART_TIMELINE_RENDERER.md",
  "product_lab/indicators/gartal_terminal/obsidian/implementation/stage_04_chart_timeline_renderer.md",
  "product_lab/indicators/gartal_terminal/obsidian/implementation/stage_04/00_STAGE_04_INDEX.md"
)

foreach ($path in $required) {
  if (!(Test-Path $path)) {
    throw "Missing required Stage 04 file: $path"
  }
}

$timeline = Get-Content "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsTimeline.mqh" -Raw
$mustContain = @(
  "GT_RenderTimelineDangerZone",
  "GT_RenderTimelineEventLabel",
  "GT_RenderTimelineBottomTape",
  "GT_DeleteObjectsByPrefix",
  "GT_ShouldRenderTimelineEvent"
)
foreach ($needle in $mustContain) {
  if ($timeline -notmatch [regex]::Escape($needle)) {
    throw "Stage 04 timeline module missing symbol: $needle"
  }
}

$inputs = Get-Content "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsInputs.mqh" -Raw
foreach ($needle in @("InpTimelineProjectionMinutes", "InpPreNewsZoneMinutes", "InpPostNewsZoneMinutes", "InpShowEventLabels")) {
  if ($inputs -notmatch [regex]::Escape($needle)) {
    throw "Stage 04 inputs missing: $needle"
  }
}

Write-Host "Gartal Terminal Stage 04 structural check passed." -ForegroundColor Green
Write-Host "Next: compile product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5 in MetaEditor." -ForegroundColor Cyan
