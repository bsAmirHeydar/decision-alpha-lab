param(
  [Parameter(Mandatory=$true)][string]$DatasetCsv,
  [string]$Target = "label_direction_60",
  [string]$Asset = "NAS100",
  [string]$Timeframe = "M1",
  [ValidateSet("extra_trees","random_forest","gradient_boosting","logit")][string]$ModelType = "extra_trees",
  [double]$TestFraction = 0.25,
  [int]$NEstimators = 500,
  [int]$MaxDepth = 8,
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
python "$PSScriptRoot\train_astro_meta_learner.py" `
  --dataset-csv $DatasetCsv `
  --target $Target `
  --asset $Asset `
  --timeframe $Timeframe `
  --common-files $Common `
  --model-type $ModelType `
  --test-fraction $TestFraction `
  --n-estimators $NEstimators `
  --max-depth $MaxDepth

if ($OpenAfter) {
  $Latest = Join-Path $Common "astro_ml\memory\$Asset\$Timeframe\latest_run.txt"
  if (Test-Path $Latest) {
    $RunId = Get-Content $Latest -Raw
    $RunId = $RunId.Trim()
    $Report = Join-Path $Common "astro_ml\memory\$Asset\$Timeframe\runs\$RunId\training_report.xlsx"
    if (Test-Path $Report) { Start-Process $Report }
  }
}
