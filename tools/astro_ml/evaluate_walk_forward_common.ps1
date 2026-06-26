param(
  [Parameter(Mandatory=$true)][string]$DatasetCsv,
  [string]$Target = "label_direction_60",
  [string]$Asset = "NAS100",
  [string]$Timeframe = "M1",
  [ValidateSet("extra_trees","random_forest","gradient_boosting","logit")][string]$ModelType = "extra_trees",
  [int]$TrainDays = 120,
  [int]$TestDays = 20,
  [int]$StepDays = 20,
  [int]$EmbargoBars = 120,
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$OutDir = Join-Path $Common "astro_ml\reports\$Asset\$Timeframe\walkforward_$Target"
python "$PSScriptRoot\evaluate_walk_forward.py" `
  --dataset-csv $DatasetCsv `
  --target $Target `
  --asset $Asset `
  --timeframe $Timeframe `
  --common-files $Common `
  --out-dir $OutDir `
  --model-type $ModelType `
  --train-days $TrainDays `
  --test-days $TestDays `
  --step-days $StepDays `
  --embargo-bars $EmbargoBars
if ($OpenAfter) {
  $Report = Join-Path $OutDir "walkforward_report.xlsx"
  if (Test-Path $Report) { Start-Process $Report }
}
