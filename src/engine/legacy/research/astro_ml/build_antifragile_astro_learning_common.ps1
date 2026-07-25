param(
  [Parameter(Mandatory=$true)][string]$DatasetCsv,
  [string]$Asset = "NAS100",
  [string]$Timeframe = "M1",
  [string]$Targets = "",
  [string]$OutDir = "",
  [double]$TestFraction = 0.25,
  [int]$MinRuleSupport = 120,
  [int]$MinOosSupport = 40,
  [double]$MinLift = 1.08,
  [double]$MaxGap = 0.14,
  [switch]$EnableNeuralChallenger,
  [int]$NeuralMinRows = 8000,
  [switch]$OpenAfter
)
$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$Script = Join-Path $PSScriptRoot "build_antifragile_astro_learning.py"
$ArgsList = @($Script, "--dataset-csv", $DatasetCsv, "--asset", $Asset, "--timeframe", $Timeframe, "--common-files", $Common, "--test-fraction", $TestFraction, "--min-rule-support", $MinRuleSupport, "--min-oos-support", $MinOosSupport, "--min-lift", $MinLift, "--max-gap", $MaxGap, "--neural-min-rows", $NeuralMinRows)
if ($Targets -ne "") { $ArgsList += @("--targets", $Targets) }
if ($OutDir -ne "") { $ArgsList += @("--out-dir", $OutDir) }
if ($EnableNeuralChallenger) { $ArgsList += "--enable-neural-challenger" }
$out = python @ArgsList | Tee-Object -Variable lines
$dirLine = ($lines | Select-String -Pattern "^ANTIFRAGILE_MEMORY_DIR=" | Select-Object -First 1).ToString()
if ($OpenAfter -and $dirLine) {
  $dir = $dirLine.Substring("ANTIFRAGILE_MEMORY_DIR=".Length)
  Invoke-Item $dir
}
