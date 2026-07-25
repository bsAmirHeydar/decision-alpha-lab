param(
  [string]$CsvName = "astro_live_mql.csv",
  [string]$OutName = "astro_final_entry_report.xlsx",
  [string]$ConfigPath = ".\\src\\engine\\legacy\\research\\astro_feature_builder\\astro_config.example.json",
  [string[]]$Families = @("A0001", "A0002", "A0003", "A0004", "A0005", "A0006", "A0007"),
  [string]$Profile = "pure_strict_tuned",
  [switch]$AlsoCsv
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$CsvPath = Join-Path $Common $CsvName
$OutPath = Join-Path $Common ("astro\\" + $OutName)

Set-Location $ProjectRoot

$argsList = @(
  ".\tests\legacy\astro_validation\astro_final_entry_report.py",
  "--csv", $CsvPath,
  "--out-xlsx", $OutPath
)

if($ConfigPath) {
  $argsList += @("--config", $ConfigPath)
}

if($Families -and $Families.Count -gt 0) {
  $argsList += "--families"
  $argsList += $Families
}

if($Profile) {
  $argsList += @("--profile", $Profile)
}

if($AlsoCsv) {
  $argsList += "--also-csv"
}

python @argsList
Write-Host "Final entry report written to $OutPath" -ForegroundColor Green
