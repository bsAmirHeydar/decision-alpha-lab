---
title: RTHP MT5 Automation — RTHP Materialization and Existing Train Activation Handoff
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, materialization, train-activation, handoff]
---

# RTHP Materialization and Existing Train Activation Handoff

## Reuse requirement

The implementation must reuse the existing:

- Canonical RTHP Context;
- ACL-03 compiled IR;
- RTHP ContextPackage and AI-input bindings;
- RTHP feature, view, dependence, task, and label contracts;
- RTHP Train Activation;
- shared trainers and validators.

## New context-owned source mode

Add an RTHP-owned M1 source adapter without changing shared engines:

```text
data_source.mode = MT5_M1_AUTOMATIC
resolved_source_mode = PAIRED_M1_BAR_JSONL
```

The adapter either:

1. materializes directly from M1 bars; or
2. converts M1 bars into a bar-observation interface understood by the RTHP materializer.

It must **not** create synthetic ticks.

## Automatic downstream steps

After accepted source binding, the existing path automatically produces:

- cycle-instance ledger;
- reference-state ledger;
- canonical occurrence ledger;
- Hunter/Protected role-price-path ledger;
- Context observations;
- feature and label matrices;
- dependence clusters;
- immutable batch;
- trainer outputs;
- run evidence.

## Compatibility gate

A dedicated parity suite must prove that the M1 source mode preserves all Context outcomes that are identifiable from M1 and explicitly marks interval-censored timing or ambiguous order instead of fabricating precision.
