$ErrorActionPreference = "Stop"

$required = @(
  "product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsDashboardTheme.mqh",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsDashboard.mqh",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsInputs.mqh",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsTypes.mqh",
  "product_lab/indicators/gartal_terminal/spec/STAGE_05_LUXURY_DASHBOARD_UI_RENDERER.md",
  "product_lab/indicators/gartal_terminal/obsidian/implementation/stage_05_luxury_dashboard_ui_renderer.md",
  "product_lab/indicators/gartal_terminal/obsidian/implementation/stage_05/00_STAGE_05_INDEX.md"
)

foreach ($path in $required) {
  if (!(Test-Path $path)) {
    throw "Missing required Stage 05 file: $path"
  }
}

$main = Get-Content "product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5" -Raw
foreach ($needle in @(
  "GartalNewsDashboardTheme.mqh",
  "Stage 05 luxury dashboard UI renderer",
  "GT_RenderDashboard"
)) {
  if ($main -notmatch [regex]::Escape($needle)) {
    throw "Stage 05 main file missing symbol: $needle"
  }
}

$dashboard = Get-Content "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsDashboard.mqh" -Raw
foreach ($needle in @(
  "GT_RenderDashboardHeader",
  "GT_RenderDashboardNextCard",
  "GT_RenderDashboardHighCard",
  "GT_RenderDashboardMetrics",
  "GT_RenderDashboardFilterBar",
  "GT_RenderDashboardMiniTape",
  "GT_UpdateCountdowns"
)) {
  if ($dashboard -notmatch [regex]::Escape($needle)) {
    throw "Stage 05 dashboard module missing symbol: $needle"
  }
}

$inputs = Get-Content "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsInputs.mqh" -Raw
foreach ($needle in @(
  "InpDashboardMode",
  "InpDashboardWidth",
  "InpDashboardShowNextCard",
  "InpDashboardShowFilterBar",
  "InpDashboardLuxuryTheme"
)) {
  if ($inputs -notmatch [regex]::Escape($needle)) {
    throw "Stage 05 inputs missing: $needle"
  }
}

Write-Host "Gartal Terminal Stage 05 structural check passed." -ForegroundColor Green
Write-Host "Next: compile product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5 in MetaEditor." -ForegroundColor Cyan
