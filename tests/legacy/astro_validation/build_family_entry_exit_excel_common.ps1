param(
  [string]$CsvName = "astro_live_mql.csv",
  [string]$OutName = "astro_family_entry_exit_suite.xlsx",
  [string]$ConfigPath = ".\\src\\engine\\legacy\\research\\astro_feature_builder\\astro_config.example.json",
  [string[]]$Families = @("PURE", "A0001", "A0002", "A0003", "A0004", "A0005", "A0006", "A0090"),
  [switch]$AlsoCsv,
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$CsvPath = Join-Path $Common $CsvName
$ReportDir = Join-Path $Common "astro\reports"
$OutPath = Join-Path $ReportDir $OutName

New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null
Set-Location $ProjectRoot

$argsList = @(
  ".\tests\legacy\astro_validation\astro_family_entry_exit_excel_suite.py",
  "--csv", $CsvPath,
  "--out-xlsx", $OutPath
)
if($ConfigPath) { $argsList += @("--config", $ConfigPath) }
if($Families -and $Families.Count -gt 0) {
  $argsList += "--families"
  $argsList += $Families
}
if($AlsoCsv) { $argsList += "--also-csv" }

python @argsList
if($OpenAfter) {
  Start-Process $OutPath
}
