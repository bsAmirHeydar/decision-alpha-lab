# Install Phase 02

Extract the ZIP at the repository root after installing Phase 01.

```powershell
Expand-Archive `
  -Path ".\decision-alpha-lab-strategy-factory-phase02-mql5-runtime-foundation.zip" `
  -DestinationPath "." `
  -Force
```

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\run_phase02_tests.ps1
```

Then run the MetaEditor compile script documented in the Phase 02 runbook.
