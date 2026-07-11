# Install Strategy Factory Phase 00

Place the ZIP in the repository root and run:

```powershell
Expand-Archive `
  -Path ".\decision-alpha-lab-strategy-factory-phase00-current-state-audit.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  ".\decision-alpha-lab-strategy-factory-phase00-current-state-audit.zip" `
  -ErrorAction SilentlyContinue
```

## Verify

```powershell
pytest -q .\lab\11_strategy_factory\phase00_current_state_audit\tests

python .\lab\11_strategy_factory\phase00_current_state_audit\run_audit.py `
  --repo-root . `
  --output .\lab\11_strategy_factory\phase00_current_state_audit\artifacts
```
