param(
  [Parameter(Mandatory=$true)][string]$RunDir,
  [Parameter(Mandatory=$true)][string]$DatasetCsv,
  [string]$OutCsv = "",
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$cmd = @("$PSScriptRoot\predict_with_astro_memory.py", "--run-dir", $RunDir, "--dataset-csv", $DatasetCsv, "--common-files", $Common)
if (-not [string]::IsNullOrWhiteSpace($OutCsv)) { $cmd += @("--out-csv", $OutCsv) }
python @cmd
if ($OpenAfter -and -not [string]::IsNullOrWhiteSpace($OutCsv)) {
  $Xlsx = [System.IO.Path]::ChangeExtension($OutCsv, ".xlsx")
  if (-not [System.IO.Path]::IsPathRooted($Xlsx)) { $Xlsx = Join-Path $Common $Xlsx }
  if (Test-Path $Xlsx) { Start-Process $Xlsx }
}
