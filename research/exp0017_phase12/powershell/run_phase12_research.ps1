$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path "."
$OutDir = Join-Path $RepoRoot "research\exp0017_phase12\outputs"

python ".\research\exp0017_phase12\python\phase12_research_workbench.py" `
  --data-dir "." `
  --out-dir $OutDir

Write-Host "EXP0017 Phase12 research outputs written to: $OutDir"
