param(
  [Parameter(Mandatory=$true)][string]$AstroCsvName,
  [string]$PriceCsvName = "",
  [string]$Asset = "NAS100",
  [string]$Timeframe = "M1",
  [ValidateSet("sanity","direction_only","professional")][string]$Preset = "professional",
  [string]$Horizons = "30,60,120",
  [string]$Targets = "",
  [ValidateSet("extra_trees","random_forest","gradient_boosting","logit")][string]$ModelType = "extra_trees",
  [double]$TestFraction = 0.25,
  [int]$NEstimators = 700,
  [int]$MaxDepth = 10,
  [switch]$RunWalkForward,
  [int]$TrainDays = 120,
  [int]$TestDays = 20,
  [int]$StepDays = 20,
  [int]$EmbargoBars = 120,
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $ProjectRoot

$cmd = @(
  "$PSScriptRoot\run_astro_ml_protocol.py",
  "--astro-csv", $AstroCsvName,
  "--asset", $Asset,
  "--timeframe", $Timeframe,
  "--common-files", $Common,
  "--preset", $Preset,
  "--horizons", $Horizons,
  "--model-type", $ModelType,
  "--test-fraction", $TestFraction,
  "--n-estimators", $NEstimators,
  "--max-depth", $MaxDepth,
  "--train-days", $TrainDays,
  "--test-days", $TestDays,
  "--step-days", $StepDays,
  "--embargo-bars", $EmbargoBars
)
if (-not [string]::IsNullOrWhiteSpace($PriceCsvName)) { $cmd += @("--price-csv", $PriceCsvName) }
if (-not [string]::IsNullOrWhiteSpace($Targets)) { $cmd += @("--targets", $Targets) }
if ($RunWalkForward) { $cmd += @("--run-walk-forward") }

$Output = python @cmd 2>&1
$Output | ForEach-Object { Write-Host $_ }

$ProtocolDir = ($Output | Select-String "ASTRO_ML_PROTOCOL_DIR=" | Select-Object -Last 1).ToString()
if ($ProtocolDir) {
  $ProtocolDir = $ProtocolDir.Replace("ASTRO_ML_PROTOCOL_DIR=", "").Trim()
  if ($OpenAfter) {
    $Report = Join-Path $ProtocolDir "protocol_report.xlsx"
    $Markdown = Join-Path $ProtocolDir "PROTOCOL_REPORT.md"
    if (Test-Path $Report) { Start-Process $Report }
    if (Test-Path $Markdown) { Start-Process $Markdown }
  }
}
