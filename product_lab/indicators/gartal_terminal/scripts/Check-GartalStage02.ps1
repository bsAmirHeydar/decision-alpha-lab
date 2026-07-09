param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"

$required = @(
    "product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsTypes.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsStore.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsSampleData.mqh",
    "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsParser.mqh",
    "product_lab/indicators/gartal_terminal/obsidian/implementation/stage_02_event_data_model_sample_pipeline.md",
    "product_lab/indicators/gartal_terminal/obsidian/implementation/stage_02/00_STAGE_02_INDEX.md",
    "product_lab/indicators/gartal_terminal/spec/STAGE_02_EVENT_DATA_MODEL_SAMPLE_PIPELINE.md"
)

$missing = @()
foreach ($file in $required) {
    $path = Join-Path $Root $file
    if (-not (Test-Path $path)) {
        $missing += $file
    }
}

if ($missing.Count -gt 0) {
    Write-Host "gartal terminal Stage 02 check failed. Missing files:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
    exit 1
}

$main = Get-Content (Join-Path $Root "product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5") -Raw
if ($main -notmatch "GartalNewsStore.mqh" -or $main -notmatch "GartalNewsSampleData.mqh") {
    Write-Host "Stage 02 includes are not wired in GartalTerminal.mq5" -ForegroundColor Red
    exit 1
}

Write-Host "gartal terminal Stage 02 file check passed." -ForegroundColor Green
Write-Host "Next: compile GartalTerminal.mq5 in MetaEditor." -ForegroundColor Cyan
