param([string]$RepoRoot=".")
$ErrorActionPreference="Stop"
python "$RepoRoot/tools/engineering/run_engineering_policy.py" "$RepoRoot"
python "$RepoRoot/src/engine/tooling/strategy_factory/check_sf20_boundaries.py" "$RepoRoot"
python "$RepoRoot/src/engine/tooling/strategy_factory/check_sf20_mql5_static.py" "$RepoRoot"
pytest -q "$RepoRoot/tests/legacy/strategy_factory/v1/phase20_integration"
python -m compileall -q "$RepoRoot/src/engine/packages/strategy_factory_integration"
Write-Host "Phase 20 preflight PASS"
