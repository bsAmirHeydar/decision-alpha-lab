# Install EXP0018 Phase00 Doctrine Freeze v2 Patch

## Scope

Documentation, ADR, registries, validation tooling and Obsidian only. No MQL5 strategy code is changed.

## Validate

```powershell
.\lab\10_infrastructure\EXP0018_daye_trader\powershell\run_exp0018_phase00_doctrine_v2_checks.ps1 -RepoRoot "."
```

## Approval step

Open:

```text
docs/execution/EXP0018_daye_trader_intermarket_divergence/
implementation_design_v2/07_phase00_doctrine_freeze_v2/
15_ARCHITECT_DECISION_WORKBOOK.md
```

Fill the final answers, then update ADR status and approval fields atomically.
