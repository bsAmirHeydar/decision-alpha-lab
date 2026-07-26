---
title: "V4-25 057 — Stationary Drift Class"
status: accepted-reference
version: 1.0.0
phase: SAED_V4_25
created: '2026-07-16'
updated: '2026-07-16'
tags:
  - saed-v4
  - v4-25
  - continual-meta-transfer
  - drift
---

# Stationary Drift Class

## Control objective

The drift layer converts changes in frozen meta-features into a deterministic taxonomy. Thresholds are ordered and versioned. Ambiguous, unsupported, or extreme shifts resolve to the novel class and therefore activate fail-closed transfer behavior.

The objective of **Stationary Drift Class** is to make this boundary explicit, machine-checkable, and reproducible. The control is evaluated before any downstream artifact can be accepted. Unknown fields, missing identities, non-finite values, future-known inputs, protected-evidence access, or authority escalation invalidate the artifact rather than being silently coerced.

## Canonical contract

The canonical contract is closed under JSON Schema Draft 2020-12 and is mirrored by exact-field Python validation. Object fields are enumerated; `additionalProperties` is false; list and numeric dimensions are frozen by the phase configuration. Identities are derived from canonical JSON and SHA-256, so equivalent content produces the same identity and any material mutation produces a different receipt.

Required invariants for this control are:

1. chronology and known-time ordering remain explicit;
2. support-side information is separated from protected query outcomes;
3. the manual or scratch baseline remains recoverable without reconstruction;
4. all resource use is charged to a frozen research budget;
5. failures resolve to a research-safe fallback;
6. UCEE remains the authority of record.

## Deterministic reference implementation

The Python reference implementation is dependency-light and deterministic. It uses canonical sorting, fixed tie-breaking, explicit threshold ordering, and content-addressed outputs. The implementation is intentionally transparent rather than optimized for scale. A future challenger may replace the numerical method only behind the same contract and only if it reproduces the golden fixture and preserves all authority boundaries.

The MQL5 files in this phase are static mirrors of constants, structures, hash fields, and fail-closed semantics. They are not runtime parity evidence. A successful static check proves naming and boundary consistency only; MetaEditor compilation and Python/MQL5 differential replay remain external gates.

## Failure and fallback semantics

Failure is conservative. Missing upstream evidence, hash mismatch, unsupported role overlap, future-source selection, insufficient support, novel drift, excessive meta-distance, budget exhaustion, query-outcome access, or an unknown contract field aborts the path. When the transfer path is merely unsupported rather than malformed, the explicit fallback is `scratch_baseline`; when the artifact is malformed, no artifact is issued.

No fallback can grant live authority. The safe result is a research receipt describing why transfer was rejected, not a hidden change to a production policy.

## Evidence and validation

Evidence for this control is supplied by positive, negative, mutation, determinism, schema, Obsidian-link, static-MQL5, boundary, and golden-reproduction checks. The evidence bundle records local test counts and artifact hashes. Claims excluded from the bundle include real alpha, prospective success, exchangeability in live markets, production calibration, runtime parity, broker qualification, and live execution safety.

## Authority boundary

This note does not authorize trading. Decision, promotion, runtime, risk allocation, execution, order submission, online learning, and production flags remain false. The output is suitable only for offline research and for the frozen handoff to V4-26 mechanistic interpretability.

## Navigation

- Previous: [[056_Drift_Taxonomy_Contract]]
- Phase map: [[00_MOC_V4_25_Continual_Meta_And_Transfer]]
- Next: [[058_Gradual_Drift_Class]]
- Program: [[V4_25_Continual_Meta_And_Transfer]]
