param([string]$RepoRoot=(Resolve-Path "$PSScriptRoot/../..").Path)
$ErrorActionPreference='Stop'
$env:PYTHONPATH=Join-Path $RepoRoot 'lab/11_strategy_factory/python'
python -m compileall (Join-Path $RepoRoot 'lab/11_strategy_factory/python/strategy_factory_deep_views_v3')
python -m pytest -q (Join-Path $RepoRoot 'lab/11_strategy_factory/tests/phase_uce_i10_deep_views')
python (Join-Path $RepoRoot 'tools/strategy_factory/check_uce_i10_boundaries.py') $RepoRoot
python (Join-Path $RepoRoot 'tools/strategy_factory/check_uce_i10_mql5_static.py') $RepoRoot
python (Join-Path $RepoRoot 'tools/strategy_factory/generate_uce_i10_vectors.py') $RepoRoot --verify-only
python (Join-Path $RepoRoot 'tools/strategy_factory/validate_uce_i10_delivery.py') $RepoRoot
