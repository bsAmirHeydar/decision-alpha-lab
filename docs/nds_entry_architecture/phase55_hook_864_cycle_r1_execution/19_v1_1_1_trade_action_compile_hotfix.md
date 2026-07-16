---
title: "Phase 55 — v1.1.1 Trade Action Compile-Surface Hotfix"
tags: [nds, hook, phase55, mql5, compile-hotfix]
status: implemented_reference_external_compile_pending
doc_version: 1.1.1
last_updated: 2026-07-16
---
# v1.1.1 Trade Action Compile-Surface Hotfix

## Incident

MetaEditor reported:

```text
undeclared identifier 'FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT_READY'
FP_NDSBacktestEngine.mqh line 103
```

## Root cause

The canonical enum in `FP_NDSHookTradeTypes.mqh` defines:

```text
FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT
```

The v1.1 Backtest statistics adapter referenced a stale, non-existent alias:

```text
FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT_READY
```

The execution engine itself already emits the canonical `PAPER_LIMIT` action. Therefore the defect was limited to statistics classification, but it blocked compilation of the complete Backtest Expert.

## Correction

`FP_NDSBacktestUpdateStats()` now compares against the canonical enum member:

```text
FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT
```

No action value, execution transition, setup rule, order path, risk geometry, or persistence behavior changed.

## Regression prevention

The Phase 55 contract QA now scans every `.mqh` and `.mq5` file under `mql5/` for `FP_NDS_HOOK_TRADE_ACTION_*` references and compares them with the canonical definitions in `FP_NDSHookTradeTypes.mqh`.

The gate fails when any stale or undeclared trade-action identifier is present.

## Verification boundary

Repository QA proves identifier closure and source consistency. Windows MetaEditor compilation remains the external acceptance gate.

## Links

- [[17_no_trade_root_cause_and_engine_fix]]
- [[18_phase04_closure_and_first_arrival_contract]]
- [[NDS Hook 86.4 No Trade Diagnostic Funnel]]
