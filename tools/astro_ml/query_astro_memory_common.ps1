param(
  [string]$Asset = "NAS100",
  [string]$Timeframe = "M1",
  [string]$Contains = "",
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$cmd = @("$PSScriptRoot\query_astro_memory.py", "--asset", $Asset, "--timeframe", $Timeframe, "--common-files", $Common)
if (-not [string]::IsNullOrWhiteSpace($Contains)) { $cmd += @("--contains", $Contains) }
python @cmd
if ($OpenAfter) {
  $Report = Join-Path $Common "astro_ml\memory\$Asset\$Timeframe\memory_query.xlsx"
  if (Test-Path $Report) { Start-Process $Report }
}
