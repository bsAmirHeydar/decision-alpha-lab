param([string]$RepoRoot=(Resolve-Path "$PSScriptRoot/../..").Path)
$ErrorActionPreference='Stop'
$env:PYTHONPATH=Join-Path $RepoRoot 'src/engine/packages'
python -m compileall (Join-Path $RepoRoot 'src/engine/packages/strategy_factory_deep_views_v3')
python -m pytest -q (Join-Path $RepoRoot 'tests/legacy/strategy_factory/v1/phase_uce_i10_deep_views')
python (Join-Path $RepoRoot 'src/engine/tooling/strategy_factory/check_uce_i10_boundaries.py') $RepoRoot
python (Join-Path $RepoRoot 'src/engine/tooling/strategy_factory/check_uce_i10_mql5_static.py') $RepoRoot
python (Join-Path $RepoRoot 'src/engine/tooling/strategy_factory/generate_uce_i10_vectors.py') $RepoRoot --verify-only
python (Join-Path $RepoRoot 'src/engine/tooling/strategy_factory/validate_uce_i10_delivery.py') $RepoRoot
