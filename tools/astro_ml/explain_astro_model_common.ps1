param(
  [Parameter(Mandatory=$true)][string]$RunDir,
  [string]$DatasetCsv = "",
  [string]$PositiveLabel = "",
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$cmd = @("$PSScriptRoot\explain_astro_model.py", "--run-dir", $RunDir, "--common-files", $Common)
if (-not [string]::IsNullOrWhiteSpace($DatasetCsv)) { $cmd += @("--dataset-csv", $DatasetCsv) }
if (-not [string]::IsNullOrWhiteSpace($PositiveLabel)) { $cmd += @("--positive-label", $PositiveLabel) }
python @cmd
if ($OpenAfter) {
  $Report = Join-Path $RunDir "explainability_report.xlsx"
  if (-not [System.IO.Path]::IsPathRooted($Report)) { $Report = Join-Path $Common $Report }
  if (Test-Path $Report) { Start-Process $Report }
}
