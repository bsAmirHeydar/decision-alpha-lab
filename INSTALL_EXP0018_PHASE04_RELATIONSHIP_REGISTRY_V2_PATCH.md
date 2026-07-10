# Install EXP0018 Phase 04 — Declarative 22-Relationship Registry v2

## Dependency order

Install P01, P02, and P03 before this patch.

## Verify

```powershell
.\lab_infrastructure\EXP0018_daye_trader\powershellun_exp0018_phase04_relationship_registry_v2_checks.ps1 -RepoRoot "."
```

## Compile

```text
mql5/Experts/DayeTrader/EXP0018_Daye_Relationship_Registry_Anatomy.mq5
```

Expected gate: `0 errors, 0 warnings`, embedded tests PASS, registry 22/6/16, WW and NP blocked.

## Runtime boundary

This Expert prints/resolves relationship topology only. It must not draw lines or emit hunt, BUY/SELL, risk, or order decisions.
