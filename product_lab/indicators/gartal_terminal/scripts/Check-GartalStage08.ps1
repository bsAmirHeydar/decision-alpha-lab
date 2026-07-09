$ErrorActionPreference = "Stop"

$Required = @(
  "product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsCalendarClient.mqh",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsParser.mqh",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsInputs.mqh",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsTypes.mqh",
  "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsDiagnostics.mqh",
  "product_lab/indicators/gartal_terminal/mql5/experts/GartalNewsDownloaderEA.mq5",
  "product_lab/indicators/gartal_terminal/test_fixtures/ff_calendar_stage08_sample.xml",
  "product_lab/indicators/gartal_terminal/spec/STAGE_08_FOREX_FACTORY_SOURCE_ADAPTER_PARSER.md",
  "product_lab/indicators/gartal_terminal/obsidian/implementation/stage_08_forex_factory_source_adapter_parser.md",
  "product_lab/indicators/gartal_terminal/obsidian/implementation/stage_08/00_STAGE_08_INDEX.md"
)

$Missing = @()
foreach ($Path in $Required) {
  if (!(Test-Path $Path)) { $Missing += $Path }
}

if ($Missing.Count -gt 0) {
  Write-Host "Stage 08 check failed. Missing files:" -ForegroundColor Red
  $Missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
  exit 1
}

$Parser = Get-Content "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsParser.mqh" -Raw
$Client = Get-Content "product_lab/indicators/gartal_terminal/mql5/include/GartalNewsCalendarClient.mqh" -Raw
$EA = Get-Content "product_lab/indicators/gartal_terminal/mql5/experts/GartalNewsDownloaderEA.mq5" -Raw

$Tokens = @(
  "GT_ParseFfXmlCalendar",
  "GT_GetTagValue",
  "GT_MapFfCountryToCurrency",
  "GT_TitleLooksBreaking",
  "GT_FetchCalendarRaw",
  "GT_LoadLocalRawFile",
  "GT_FetchCalendarByWebRequest",
  "GTD_Download"
)

foreach ($Token in $Tokens) {
  if (($Parser + $Client + $EA) -notmatch [regex]::Escape($Token)) {
    Write-Host "Stage 08 check failed. Missing token: $Token" -ForegroundColor Red
    exit 1
  }
}

Write-Host "Stage 08 structure check passed." -ForegroundColor Green
Write-Host "Next: compile GartalTerminal.mq5 and GartalNewsDownloaderEA.mq5 in MetaEditor." -ForegroundColor Cyan
