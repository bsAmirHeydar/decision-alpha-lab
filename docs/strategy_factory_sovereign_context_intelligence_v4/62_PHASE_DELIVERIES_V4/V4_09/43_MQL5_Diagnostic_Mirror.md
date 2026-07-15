---
title: MQL5 Diagnostic Mirror
status: implemented-reference
phase: SAED_V4_09
version: 1.0.0
created: '2026-07-15'
updated: '2026-07-15'
capability_tier: core-production-reference
authority: reference-only
tags:
  - saed-v4
  - v4-09
  - execution-digital-twin
---

# MQL5 Diagnostic Mirror

## Institutional intent

Mirror authority, types, latency, queue, lifecycle, and integrity checks without order APIs. The implementation is subordinate to immutable Context truth, the V4-08 Executable Path Outcome Cube, protected evidence roles, UCEE promotion, hard risk, portfolio governance, runtime compilation, and I18 production qualification.

## Contract and invariants

- Every artifact is exact-versioned, content-addressed, and reproducible from frozen inputs.
- Every source outcome row is preserved by `source_row_id`, `source_row_hash`, `node_id`, and `node_hash`.
- Every configured scenario produces exactly one projection for every source row; missing, duplicate, or unexpected pairs fail closed.
- Skip and Abstain remain non-order outcomes in every scenario.
- Unknown fields, unsupported evidence roles, invalid probabilities, negative costs, and authority escalation are rejected.
- V4-09 adds execution assumptions and incremental execution costs; it never rewrites V4-08 outcomes.

## Scientific and execution semantics

The reference implementation starts with deliberately simple monotone components: bounded latency realization, queue uncertainty, exponential fill-hazard decay, linear plus square-root impact, and explicit adverse-selection penalties. Complexity is not accepted merely because it fits historical fills. Any learned point-process, queue-reactive, agent-based, or broker-specific challenger must declare support, censoring, calibration, drift, transport limits, and protected evaluation evidence.

Reference-synthetic scenarios are watermarked. They can reject fragile ideas, expose sensitivity, and define engineering boundaries, but they cannot create positive alpha, promotion, prospective, shadow, broker-parity, or production claims. The digital twin is not a substitute for prospective paper, shadow operation, micro-live qualification, or recovery drills.

## Failure behavior

Failures resolve to reject, quarantine, or explicit non-order state. No implicit fallback may create a fill, change a source row, delete a scenario, rank a treatment, allocate capital, activate runtime, or send an order. Incidents retain source identity, reason code, detail, and a false recovery-authority flag.

## Evidence required

1. Closed schema validation and negative fixtures.
2. Deterministic golden build, replay, semantic diff, and Merkle receipt.
3. Complete row-by-scenario exposure accounting.
4. Python unit, mutation, property, and authority tests.
5. MQL5 static diagnostics with MetaEditor compilation separately classified.
6. Explicit limitations and unresolved external qualification gates.

## Operational review

Reviewers must verify that nominal and stress profiles are exact, source identities are untouched, incremental cost is non-negative, partial fills preserve quantity, lifecycle chains are monotone, synthetic watermarking cannot be removed, and all output authority flags remain false. Any mismatch blocks the V4-10 handoff.

## Navigation

- [[00_MOC_V4_09_Execution_Digital_Twin|V4-09 Map of Content]]
- [[61_V4_10_Baseline_Manual_Handoff|V4-10 handoff]]

## Related architecture

- [[V4_09_Execution_Digital_Twin]]
- [[Execution_Digital_Twin_Charter]]
- [[ADR_V4_014_Execution_Digital_Twin_Does_Not_Replace_Shadow]]
