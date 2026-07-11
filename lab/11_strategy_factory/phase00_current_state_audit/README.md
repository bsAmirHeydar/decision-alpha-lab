# Phase 00 Current-State Audit

This module implements the first Strategy Factory implementation gate. It inventories a clean repository checkout, classifies reusable modules, detects overlapping infrastructure, maps implicit Python contracts, scans for executable order authority, captures the current test baseline, and generates reproducible migration artifacts.

## Run

```powershell
python .\lab\11_strategy_factory\phase00_current_state_audit\run_audit.py `
  --repo-root . `
  --output .\lab\11_strategy_factory\phase00_current_state_audit\artifacts
```

The auditor is read-only with respect to the repository being scanned. It only writes to the explicit output directory.
