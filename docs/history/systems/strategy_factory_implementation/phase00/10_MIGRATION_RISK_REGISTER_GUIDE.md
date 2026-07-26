---
title: "Migration Risk Register Guide"
tags: [strategy-factory, phase-00, risk-register]
status: canonical
---

# Migration Risk Register Guide

The canonical machine-readable register is:

```text
lab/11_strategy_factory/phase00_current_state_audit/artifacts/migration_risk_register.json
```

## Critical risk

### RISK-005 — Terminal-local and naive timestamps

Evidence:

- connector labels timezone as `terminal` rather than canonical UTC;
- synchronization uses `datetime.now()`;
- no explicit broker/exchange timezone or DST version exists.

Impact:

An anatomy event can be correct in price but wrong in time. Walk-forward folds, session logic, multi-symbol alignment, feature known-time, and outcome horizons can all leak or misalign.

Owner: Phase 07.

## High risks

### RISK-002 — Clean-checkout test collection fails

Owner: Phase 02.

### RISK-003 — Generated artifacts are committed as source

Owner: Phase 05.

### RISK-004 — Three persistence conventions

Owner: Phase 05.

### RISK-006 — M0001 interface drift

Owner: Phase 01.

### RISK-008 — Tests require live MT5

Owner: Phase 06.

### RISK-009 — Missing full strategy programs

The uploaded snapshot does not contain EXP0017 or NDS. Owner: Phase 20/21 integration planning.

## Medium risk

### RISK-007 — Empty registries and lifecycle shells

Owner: Phase 04.

## Low risk

### RISK-010 — Runtime caches tracked

Owner: Phase 02.

## Controlled condition

### RISK-001 — No live order authority present

This is not a defect. It is a controlled baseline that must be preserved until the broker-boundary phase.

## Register governance

- Risk IDs are immutable.
- Closing a risk requires evidence, not a comment.
- Severity may change only with rationale.
- Every open risk has one owner phase.
- A phase may not close while owning an unresolved blocker.
- Deferred risks remain visible in acceptance reports.
