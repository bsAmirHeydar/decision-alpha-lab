param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$Python = Get-Command python -ErrorAction Stop
& $Python.Source "$RepoRoot/lab/10_infrastructure/EXP0018_daye_trader/tools/validate_exp0018_phase07_reference_lifecycle_v2.py"
& $Python.Source -m pytest "$RepoRoot/lab/10_infrastructure/EXP0018_daye_trader/tests/test_exp0018_phase07_reference_lifecycle_v2.py" -q
Write-Host "EXP0018 Phase 07 checks complete. Compile the P07 Expert in MetaEditor and require 0 errors, 0 warnings."
