param(
  [string]$CsvName = "astro_live_mql.csv",
  [string]$OutFolder = "astro_suite_validation",
  [string]$ConfigPath = ".\\src\\engine\\legacy\\research\\astro_feature_builder\\astro_config.example.json",
  [string[]]$Families = @("A0001", "A0002", "A0003", "A0004", "A0005", "A0006", "A0007", "A0090")
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$CsvPath = Join-Path $Common $CsvName
$OutDir = Join-Path $Common ("astro\validation\" + $OutFolder)

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
Set-Location $ProjectRoot

$argsList = @(
  ".\tests\legacy\astro_validation\astro_family_validation_suite.py",
  "--csv", $CsvPath,
  "--out-dir", $OutDir
)

if($ConfigPath) {
  $argsList += @("--config", $ConfigPath)
}

if($Families -and $Families.Count -gt 0) {
  $argsList += "--families"
  $argsList += $Families
}

python @argsList
Write-Host "Suite validation outputs written to $OutDir" -ForegroundColor Green
