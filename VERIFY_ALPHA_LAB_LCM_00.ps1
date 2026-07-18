$ErrorActionPreference = "Stop"
$baselineRoot = Get-ChildItem -Path ".\registry\legacy_context_migration\baselines" -Directory -Filter "BASELINE_*" | Sort-Object Name | Select-Object -Last 1
if (-not $baselineRoot) { throw "LCM-00 baseline package not found." }
python -m tools.strategy_factory.lcm.lcm_00.cli verify-package --package-root $baselineRoot.FullName
python -m pytest -q ".\lab\11_strategy_factory\migration\tests_lcm_00"
