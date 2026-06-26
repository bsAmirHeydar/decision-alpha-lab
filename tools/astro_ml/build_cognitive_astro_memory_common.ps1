param(
  [Parameter(Mandatory=$true)][string]$DatasetCsv,
  [string]$Asset = "NAS100",
  [string]$Timeframe = "M1",
  [string]$Targets = "",
  [int]$MinSupport = 80,
  [double]$MinLift = 1.10,
  [double]$MaxStabilityGap = 0.18,
  [switch]$OpenAfter
)
$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$Script = Join-Path $PSScriptRoot "build_cognitive_astro_memory.py"
$ArgsList = @($Script, "--dataset-csv", $DatasetCsv, "--asset", $Asset, "--timeframe", $Timeframe, "--common-files", $Common, "--min-support", $MinSupport, "--min-lift", $MinLift, "--max-stability-gap", $MaxStabilityGap)
if ($Targets -ne "") { $ArgsList += @("--targets", $Targets) }
$out = python @ArgsList | Tee-Object -Variable lines
$dirLine = ($lines | Select-String -Pattern "^COGNITIVE_MEMORY_DIR=" | Select-Object -First 1).ToString()
if ($OpenAfter -and $dirLine) {
  $dir = $dirLine.Substring("COGNITIVE_MEMORY_DIR=".Length)
  Invoke-Item $dir
}
