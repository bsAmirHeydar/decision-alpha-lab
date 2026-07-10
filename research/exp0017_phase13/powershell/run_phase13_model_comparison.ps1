param(
  [string]$DataDir = ".",
  [string]$OutDir = ".\research\exp0017_phase13\outputs",
  [string]$DatasetFile = "EXP0017_Phase10_Model_Dataset.csv",
  [string]$FoldPlanFile = "EXP0017_Phase11_Fold_Plan.csv",
  [string]$IntegritySummary = "research\exp0017_phase12_5\outputs\phase12_5_readiness_summary.json",
  [int]$Seed = 170013,
  [switch]$AllowMissingIntegrity,
  [switch]$NoPredictions
)

$ErrorActionPreference = "Stop"
$Script = Join-Path $PSScriptRoot "..\python\phase13_controlled_model_comparison.py"
$Args = @(
  $Script,
  "--data-dir", $DataDir,
  "--out-dir", $OutDir,
  "--dataset-file", $DatasetFile,
  "--fold-plan-file", $FoldPlanFile,
  "--integrity-summary", $IntegritySummary,
  "--seed", $Seed
)
if ($AllowMissingIntegrity) { $Args += "--allow-missing-integrity" }
if ($NoPredictions) { $Args += "--no-write-predictions" }
python @Args
exit $LASTEXITCODE
