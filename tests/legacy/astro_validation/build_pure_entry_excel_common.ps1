param(
  [string]$CsvName = "astro_nas100_mql.csv",
  [string]$OutName = "nas100_pure_entry_windows.xlsx",
  [ValidateSet("PURE", "A0001", "A0002", "A0003", "A0090")]
  [string]$Family = "PURE",
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
  ".\tests\legacy\astro_validation\astro_pure_entry_excel.py",
  "--csv", $CsvPath,
  "--out-xlsx", $OutPath,
  "--family", $Family
)
if($AlsoCsv) { $argsList += "--also-csv" }

python @argsList

if($OpenAfter) {
  Start-Process $OutPath
}
