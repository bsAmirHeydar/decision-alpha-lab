# Install Strategy Factory V2

Place the ZIP in the repository root, next to the `lab` and `docs` directories.

```powershell
Expand-Archive `
  -Path ".\decision-alpha-lab-strategy-factory-v2-ultra-modular-patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  ".\decision-alpha-lab-strategy-factory-v2-ultra-modular-patch.zip" `
  -ErrorAction SilentlyContinue
```

This artifact is standalone. Installing the old Strategy Factory patch first is not required. If V1 was already installed, V2 intentionally upgrades the same shared module and adds new V2 directories.

## Verify

```powershell
python -m compileall `
  .\lab\11_strategy_factory\python

pytest -q `
  .\lab\11_strategy_factory\tests `
  .\lab\11_strategy_factory\tests_v2

python .\lab\11_strategy_factory\sf.py compile-v2 `
  .\lab\11_strategy_factory\examples\manifests_v2\temporal_divergence_fast.json

python .\lab\11_strategy_factory\sf.py decide-v2 `
  .\lab\11_strategy_factory\examples\manifests_v2\temporal_divergence_fast.json

python .\lab\11_strategy_factory\sf.py benchmark-v2 `
  .\lab\11_strategy_factory\examples\manifests_v2\temporal_divergence_fast.json `
  --warmup 100 `
  --iterations 1000
```

## Scaffold a new anatomy

```powershell
python .\lab\11_strategy_factory\sf.py scaffold-v2 `
  EXP0019_new_anatomy `
  --output-root .\lab\03_experiments
```

## Canonical documentation

```text
docs\strategy_factory_v2\00_start_here\00_STRATEGY_FACTORY_V2_MOC.md
```
