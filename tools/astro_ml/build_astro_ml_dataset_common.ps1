param(
  [Parameter(Mandatory=$true)][string]$AstroCsvName,
  [string]$PriceCsvName = "",
  [string]$Asset = "NAS100",
  [string]$Timeframe = "M1",
  [string]$OutName = "",
  [string]$Horizons = "30,60,120",
  [double]$DirectionThresholdPct = 0.0010,
  [double]$SpikeThresholdPct = 0.0030,
  [double]$TrapTriggerPct = 0.0015,
  [double]$CleanMinMfePct = 0.0015,
  [double]$CleanMaxMaePct = 0.0008,
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$Reports = Join-Path $Common "astro_ml\reports\$Asset\$Timeframe"
New-Item -ItemType Directory -Force -Path $Reports | Out-Null

if ([string]::IsNullOrWhiteSpace($OutName)) {
  $OutName = "astro_ml_dataset_${Asset}_${Timeframe}.csv"
}
$OutCsv = Join-Path $Reports $OutName
$OutXlsx = [System.IO.Path]::ChangeExtension($OutCsv, ".xlsx")

$cmd = @(
  "$PSScriptRoot\build_astro_ml_dataset.py",
  "--astro-csv", $AstroCsvName,
  "--asset", $Asset,
  "--timeframe", $Timeframe,
  "--common-files", $Common,
  "--out-csv", $OutCsv,
  "--out-xlsx", $OutXlsx,
  "--horizons", $Horizons,
  "--direction-threshold-pct", $DirectionThresholdPct,
  "--spike-threshold-pct", $SpikeThresholdPct,
  "--trap-trigger-pct", $TrapTriggerPct,
  "--clean-min-mfe-pct", $CleanMinMfePct,
  "--clean-max-mae-pct", $CleanMaxMaePct
)
if (-not [string]::IsNullOrWhiteSpace($PriceCsvName)) {
  $cmd += @("--price-csv", $PriceCsvName)
}
python @cmd
if ($OpenAfter) { Start-Process $OutXlsx }
