param(
  [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"
$ResolvedRoot = (Resolve-Path $RepoRoot).Path

python "$ResolvedRoot\contexts\legacy\infrastructure\exp0018_daye_trader\tools\validate_exp0018_phase04_relationship_registry_v2.py" "$ResolvedRoot"
python -m pytest "$ResolvedRoot\contexts\legacy\infrastructure\exp0018_daye_trader\tests\test_exp0018_phase04_relationship_registry_v2.py" -q
python -m py_compile `
  "$ResolvedRoot\contexts\legacy\infrastructure\exp0018_daye_trader\tools\validate_exp0018_phase04_relationship_registry_v2.py" `
  "$ResolvedRoot\contexts\legacy\infrastructure\exp0018_daye_trader\tests\test_exp0018_phase04_relationship_registry_v2.py"

Write-Host "EXP0018 Phase04 relationship registry checks passed." -ForegroundColor Green
