---
title: "Rollback, Change Control, and Re-Audit"
tags: [strategy-factory, phase-00, rollback, change-control]
status: canonical
---

# Rollback, Change Control, and Re-Audit

## Rollback principle

Phase 00 adds only a read-only auditor, documentation, tests, and generated evidence. Rolling it back must not alter market-data, node, metric, or execution behavior.

## Rollback procedure

Remove only the Phase 00 paths:

```text
docs/strategy_factory_implementation/phase00/
docs/obsidian_deep/00_mocs/STRATEGY_FACTORY_PHASE00_CURRENT_STATE_AUDIT_MOC.md
lab/11_strategy_factory/phase00_current_state_audit/
lab/11_strategy_factory/implementation_program/phase_status/PHASE_00.json
```

No legacy file must be deleted by the installation patch.

## Re-audit triggers

Run the audit again after:

- adding a strategy repository or patch;
- importing EXP0017, NDS, Daye, ICT, or Astro code;
- adding any MQL5 files;
- adding broker or order APIs;
- changing market-data storage;
- changing package layout;
- removing legacy caches;
- completing Phase 01 or Phase 02.

## Change classification

### Baseline-preserving change

Documentation correction, new non-authority scanner pattern, or improved report rendering.

### Baseline-changing change

New source modules, new strategy programs, execution code, cache movement, or contract changes. These require regenerated artifacts.

### Gate-changing change

Any newly discovered live authority, unclassified module, missing required artifact, or critical unowned risk. These can move the phase back to `BLOCKED`.

## Evidence retention

Each accepted audit should retain:

- Git commit;
- auditor version;
- generated artifacts;
- test environment;
- QA result;
- risk register;
- authority scan.

Old accepted audits should be archived rather than overwritten once the formal Artifact Store exists.
