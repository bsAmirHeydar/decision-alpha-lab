---
title: SAED V4-10 — Acceptance Criteria
status: implemented-reference
version: 1.0.0
created: '2026-07-15'
updated: '2026-07-15'
tags:
  - saed-v4
  - v4-10
  - baseline-manual
---

# SAED V4-10 — Acceptance Criteria

## Purpose

Acceptance requires closed schemas, deterministic replay, hostile fixture rejection, baseline preservation, complete exposure, corpus leakage exclusion, QA pass and explicit external-evidence gaps.

## Institutional contract

The contract is additive, deterministic, content-addressed and fail-closed. All upstream identities are read-only. Unknown fields, unknown feature references, forbidden evidence roles, ordinary fallbacks, incomplete exposure and any request for training, ranking, selection, risk, runtime or order authority are rejected.

## Engineering requirements

1. Inputs must carry exact phase, version, identity, evidence role and known-time lineage.
2. Outputs must preserve synthetic watermarking and explicitly state non-goals.
3. Every emitted artifact must have a stable content hash and deterministic replay path.
4. Python, JSON Schema and MQL5 mirror boundaries must agree on authority denial.
5. External evidence must never be inferred from local unit or static validation.

## Verification

Verification includes golden replay, negative fixtures, mutation/conformance vectors, schema closure, baseline exposure accounting, integrity receipt verification, semantic diff, boundary scanning, MQL5 static validation and Obsidian link checks.

## Failure behavior

Failure is deny-by-default. No partial registry, benchmark, corpus manifest or handoff may be treated as accepted. A mismatch creates an incident record and blocks V4-11.

## Residual limitation

This phase is reference-synthetic. It does not claim model training, learned representation, real alpha, prospective success, runtime parity, production qualification or live trading.

## Related artifacts

- [[45_V4_11_Handoff|V4-11 handoff]]
- [[43_Acceptance_Criteria|Acceptance criteria]]
- [[44_Limitations_And_Residual_Risk|Limitations and residual risk]]
