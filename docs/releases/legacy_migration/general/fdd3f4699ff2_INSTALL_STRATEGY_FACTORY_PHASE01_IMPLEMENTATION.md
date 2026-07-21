# Install Strategy Factory Phase 01

Extract this ZIP at the repository root. It is additive.

```powershell
Expand-Archive `
  -Path ".\decision-alpha-lab-strategy-factory-phase01-mql5-first-contracts.zip" `
  -DestinationPath "." `
  -Force
```

Then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\run_phase01_tests.ps1
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\compile_sf01_contracts.ps1 `
  -MetaEditorPath "C:\Path\To\MetaEditor64.exe"
```
