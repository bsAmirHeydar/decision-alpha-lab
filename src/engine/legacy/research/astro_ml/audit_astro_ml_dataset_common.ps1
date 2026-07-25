param(
  [Parameter(Mandatory=$true)][string]$DatasetCsv,
  [string]$Asset = "NAS100",
  [string]$Timeframe = "M1",
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$Reports = Join-Path $Common "astro_ml\reports\$Asset\$Timeframe"
New-Item -ItemType Directory -Force -Path $Reports | Out-Null
$OutXlsx = Join-Path $Reports "astro_ml_dataset_audit_${Asset}_${Timeframe}.xlsx"
$OutJson = [System.IO.Path]::ChangeExtension($OutXlsx, ".json")

python "$PSScriptRoot\astro_ml_audit_dataset.py" `
  --dataset-csv $DatasetCsv `
  --asset $Asset `
  --timeframe $Timeframe `
  --common-files $Common `
  --out-xlsx $OutXlsx `
  --out-json $OutJson

if ($OpenAfter -and (Test-Path $OutXlsx)) { Start-Process $OutXlsx }
