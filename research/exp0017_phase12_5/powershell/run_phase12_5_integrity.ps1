param(
  [string]$DataDir = ".",
  [string]$OutDir = ".\research\exp0017_phase12_5\outputs",
  [int]$MaxRows = 500000,
  [double]$ExactLineageMinPct = 99.90,
  [int]$CountTolerance = 0,
  [switch]$FailOnWarning
)

$ErrorActionPreference = "Stop"

$ArgsList = @(
  ".\research\exp0017_phase12_5\python\phase12_5_pipeline_integrity.py",
  "--data-dir", $DataDir,
  "--out-dir", $OutDir,
  "--max-rows", $MaxRows,
  "--exact-lineage-min-pct", $ExactLineageMinPct,
  "--count-tolerance", $CountTolerance
)
if ($FailOnWarning) { $ArgsList += "--fail-on-warning" }

& python @ArgsList
$ExitCode = $LASTEXITCODE
if ($ExitCode -eq 2) {
  throw "EXP0017 Phase 12.5 blocked Phase 13. Review readiness gates in $OutDir."
}
if ($ExitCode -eq 1) {
  throw "EXP0017 Phase 12.5 completed with warnings and FailOnWarning was enabled."
}
Write-Host "EXP0017 Phase 12.5 integrity audit completed. Outputs: $OutDir"
