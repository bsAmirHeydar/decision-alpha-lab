param([string]$RepoRoot=".")
$ErrorActionPreference="Stop"
python "$RepoRoot/tools/engineering/run_engineering_policy.py" "$RepoRoot"
python "$RepoRoot/tools/strategy_factory/check_sf20_boundaries.py" "$RepoRoot"
python "$RepoRoot/tools/strategy_factory/check_sf20_mql5_static.py" "$RepoRoot"
pytest -q "$RepoRoot/lab/11_strategy_factory/tests/phase20_integration"
python -m compileall -q "$RepoRoot/lab/11_strategy_factory/python/strategy_factory_integration"
Write-Host "Phase 20 preflight PASS"
