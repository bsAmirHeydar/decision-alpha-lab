# Strategy Factory Phase 14 — Model Registry, Promotion and Artifact Governance

Phase 14 converts immutable validation and training evidence into a governed model registry. It adds exact registry scopes, artifact inventories, integrity and authenticity separation, versioned promotion policies, deterministic gate evaluations, immutable registry entries, legal state transitions, one-champion-per-scope enforcement, append-only hash-chained decisions, registry snapshots, model release manifests and explicit rollback plans.

MQL5 remains the terminal-side typed contract authority. Python performs offline file hashing, policy evaluation, governance reporting and fixture generation. Neither side receives execution, risk or capital authority in this phase.

## Verification

```powershell
powershell -ExecutionPolicy Bypass -File .	ools\strategy_factory
un_phase14_tests.ps1
powershell -ExecutionPolicy Bypass -File .	ools\strategy_factory\compile_sf14_governance.ps1 -MetaEditor "C:\Program Files\MetaTrader 5\metaeditor64.exe"
```
