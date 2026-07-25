param(
  [Parameter(Mandatory=$true)][string]$DatasetCsv,
  [string]$Asset = "NAS100",
  [string]$Timeframe = "M1",
  [string]$AntifragileDir = "",
  [string]$Targets = "",
  [int]$Folds = 6,
  [int]$MinFoldSupport = 25,
  [double]$MinSurvivalRate = 0.60,
  [double]$MinMedianLift = 1.05,
  [double]$MinWorstLift = 0.95,
  [double]$MaxLiftIqr = 0.65,
  [int]$PerturbRepeats = 24,
  [double]$PerturbNoiseScale = 0.035,
  [double]$PerturbDropoutRate = 0.10,
  [double]$MaxPerturbDrop = 0.055,
  [double]$MaxConceptDependencyDrop = 0.12,
  [int]$MaxRulesPerTarget = 12,
  [int]$MaxRulesPerConceptTarget = 4,
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$Script = Join-Path $PSScriptRoot "build_antifragile_fragility_audit.py"

$argsList = @(
  $Script,
  "--dataset-csv", $DatasetCsv,
  "--asset", $Asset,
  "--timeframe", $Timeframe,
  "--common-files", $Common,
  "--folds", "$Folds",
  "--min-fold-support", "$MinFoldSupport",
  "--min-survival-rate", "$MinSurvivalRate",
  "--min-median-lift", "$MinMedianLift",
  "--min-worst-lift", "$MinWorstLift",
  "--max-lift-iqr", "$MaxLiftIqr",
  "--perturb-repeats", "$PerturbRepeats",
  "--perturb-noise-scale", "$PerturbNoiseScale",
  "--perturb-dropout-rate", "$PerturbDropoutRate",
  "--max-perturb-drop", "$MaxPerturbDrop",
  "--max-concept-dependency-drop", "$MaxConceptDependencyDrop",
  "--max-rules-per-target", "$MaxRulesPerTarget",
  "--max-rules-per-concept-target", "$MaxRulesPerConceptTarget"
)
if ($AntifragileDir -ne "") { $argsList += @("--antifragile-dir", $AntifragileDir) }
if ($Targets -ne "") { $argsList += @("--targets", $Targets) }

$output = & python @argsList
$output | Write-Host

if ($OpenAfter) {
  $report = ($output | Select-String -Pattern "^FRAGILITY_AUDIT_REPORT=(.+)$").Matches.Groups[1].Value
  if ($report -and (Test-Path $report)) { Start-Process $report }
}
