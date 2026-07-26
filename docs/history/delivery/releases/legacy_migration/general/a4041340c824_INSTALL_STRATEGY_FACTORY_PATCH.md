# Install the Strategy Factory patch

Place `decision-alpha-lab-strategy-factory-deep-patch.zip` in the repository
root, where `AGENTS.md`, `docs`, and `lab` are located.

```powershell
Expand-Archive `
  -Path ".\decision-alpha-lab-strategy-factory-deep-patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  ".\decision-alpha-lab-strategy-factory-deep-patch.zip" `
  -ErrorAction SilentlyContinue
```

## Verify

```powershell
python -m compileall `
  .\lab\11_strategy_factory\python

pytest -q `
  .\lab\11_strategy_factory\tests

python .\lab\11_strategy_factory\sf.py validate-manifest `
  .\lab\11_strategy_factory\examples\manifests\temporal_divergence.json

python .\tools\engineering\check_mql5_compatibility.py .
python .\tools\engineering\validate_alpha_lab_policy.py .
```

## Stage only patch project files

```powershell
git add -- `
  "docs/strategy_factory" `
  "docs/obsidian_deep/00_mocs/STRATEGY_FACTORY_MOC.md" `
  "lab/11_strategy_factory" `
  "docs/releases/legacy_migration/general/5ef574d86cf8_README_STRATEGY_FACTORY_PATCH.md" `
  "docs/releases/legacy_migration/general/a4041340c824_INSTALL_STRATEGY_FACTORY_PATCH.md" `
  "STRATEGY_FACTORY_PATCH_MANIFEST.json" `
  "STRATEGY_FACTORY_QA_REPORT.json" `
  "STRATEGY_FACTORY_FILE_INDEX.txt" `
  "STRATEGY_FACTORY_FILE_HASHES.sha256" `
  "COMMIT_MESSAGE.md"
```
