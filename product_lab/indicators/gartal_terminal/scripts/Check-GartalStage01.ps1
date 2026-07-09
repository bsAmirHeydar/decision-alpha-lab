param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"

$required = @(
    "product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsTypes.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsUtils.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsInputs.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsTime.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsDiagnostics.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsCalendarClient.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsParser.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsDashboard.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsTimeline.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsAlerts.mqh"
)

$missing = @()
foreach ($item in $required) {
    $path = Join-Path $Root $item
    if (-not (Test-Path $path)) {
        $missing += $item
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Missing Stage 01 files:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
    exit 1
}

Write-Host "gartal terminal Stage 01 file check passed." -ForegroundColor Green
Write-Host "Open this file in MetaEditor:" -ForegroundColor Cyan
Write-Host "product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5" -ForegroundColor Cyan
