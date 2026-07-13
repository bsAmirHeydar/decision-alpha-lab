param([string]$RepoRoot=".")
$ErrorActionPreference="Stop";$root=(Resolve-Path $RepoRoot).Path;$env:PYTHONPATH=(Join-Path $root "lab\11_strategy_factory\python")
python (Join-Path $root "tools\engineering\run_engineering_policy.py") $root
python (Join-Path $root "tools\strategy_factory\check_uce_i08_boundaries.py") $root
python (Join-Path $root "tools\strategy_factory\check_uce_i08_mql5_static.py") $root
python (Join-Path $root "tools\strategy_factory\validate_uce_i08_delivery.py") $root
python -m compileall -q (Join-Path $root "lab\11_strategy_factory\python\strategy_factory_classical_v3")
python -m strategy_factory_classical_v3.cli conformance
python (Join-Path $root "tools\strategy_factory\generate_uce_i08_vectors.py") $root --verify-only
pytest -q --import-mode=importlib `
 (Join-Path $root "lab\11_strategy_factory\tests\phase_uce_i01_contracts") `
 (Join-Path $root "lab\11_strategy_factory\tests\phase_uce_i02_contexts") `
 (Join-Path $root "lab\11_strategy_factory\tests\phase_uce_i03_treatments") `
 (Join-Path $root "lab\11_strategy_factory\tests\phase_uce_i04_treatment_compiler") `
 (Join-Path $root "lab\11_strategy_factory\tests\phase_uce_i05_economics") `
 (Join-Path $root "lab\11_strategy_factory\tests\phase_uce_i06_dataset") `
 (Join-Path $root "lab\11_strategy_factory\tests\phase_uce_i07_trainers") `
 (Join-Path $root "lab\11_strategy_factory\tests\phase_uce_i08_classical")
