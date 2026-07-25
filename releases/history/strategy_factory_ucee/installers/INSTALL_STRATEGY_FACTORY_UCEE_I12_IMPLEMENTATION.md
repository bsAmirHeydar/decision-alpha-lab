# Install UCEE I12 Patch

Run the final command block from the repository root. The patch file index is the exact staging authority; unrelated working-tree changes must remain unstaged.

## Preconditions

- UCE-I11 is already present.
- Python 3.10+ is available.
- `numpy`, `pytest`, and `jsonschema` are installed for validation.
- Git remote `origin` is configured before push.

## Validation after expansion

```powershell
$env:PYTHONPATH = ".\lab\11_strategy_factory\python"
python -m pytest -q .\lab\11_strategy_factory\tests\phase_uce_i12_promotion
python .\tools\strategy_factory\check_uce_i12_boundaries.py
python .\tools\strategy_factory\check_uce_i12_mql5_static.py
python .\tools\strategy_factory\validate_uce_i12_delivery.py .
```

## Local MetaEditor gate

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\compile_uce_i12_statistical_promotion.ps1 -RepoRoot .
```

Do not mark MetaEditor as passed unless the generated logs show zero compile errors.
