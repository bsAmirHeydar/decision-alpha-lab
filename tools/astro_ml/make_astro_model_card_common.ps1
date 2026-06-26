param(
  [Parameter(Mandatory=$true)][string]$RunDir,
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
python "$PSScriptRoot\make_astro_model_card.py" --run-dir $RunDir
if ($OpenAfter) {
  $Card = Join-Path $RunDir "MODEL_CARD.md"
  $Xlsx = Join-Path $RunDir "model_card.xlsx"
  if (Test-Path $Card) { Start-Process $Card }
  if (Test-Path $Xlsx) { Start-Process $Xlsx }
}
