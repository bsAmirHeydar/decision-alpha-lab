---
title: SAED V4-22 — Negative Watermark Fixture
status: accepted-reference
version: 1.0.0
phase: SAED_V4_22
evidence_scope: local-deterministic-synthetic-reference
claim_ceiling: stress-and-falsification-only
tags:
  - saed-v4
  - v4-22
  - generative-stress
  - research-only
---

# SAED V4-22 — Negative Watermark Fixture

## Purpose

This note specifies **Negative Watermark Fixture** inside the closed V4-22 Generative Path Stress Lab. The capability exists to create deterministic, watermarked and auditable synthetic market paths that can falsify robustness claims. It does not create positive alpha evidence and it does not authorize a treatment, risk allocation, runtime generation or order.

## Normative contract

The artifact is versioned, content-addressed and bound to immutable V4-21 intake hashes. Inputs must satisfy known-time semantics, declared data roles and exact closed schemas. Unknown fields, hidden-evaluation content, protected-final evidence, missing lineage or any authority-bearing flag fail closed.

## Engineering behavior

The reference implementation uses deterministic seed derivation, canonical JSON hashing and bounded standard-library numerics. All generated paths preserve timestamp order, OHLC geometry, bid/ask order, non-negative volume, bounded liquidity and explicit synthetic watermarking. Stress transformations preserve the declared grid and retain parent-path lineage.

## Scientific controls

Synthetic paths may be used for stress discovery, failure search, sensitivity analysis and simulator-exploitation diagnostics. Synthetic gains are never counted as empirical edge. Fidelity is evaluated across return location and scale, tails, serial dependence, spread, liquidity, regime occupancy and a distinguishability proxy. Uncertainty growth defines a trusted imagination horizon rather than concealing rollout degradation.

## Failure semantics

A contract mismatch rejects the run. An invariant violation quarantines the path. A watermark failure invalidates the synthetic artifact. Excessive simulator exploitability rejects the generator-policy pairing. Budget exhaustion stops the research family. Fidelity weakness narrows permitted use to labeled stress-only analysis and cannot be waived into promotion evidence.

## UCEE authority boundary

UCEE remains sovereign. V4-22 cannot mutate Context truth, Treatment DSL, promotion admission, hybrid-policy authority, runtime compilation, portfolio risk, release qualification or broker execution. Allowed terminal responses are Skip, Abstain, Manual fallback, Reject and Quarantine.

## Required evidence

- Exact input and output hashes.
- Closed schema validation.
- Golden, negative and mutation tests.
- Deterministic replay receipt.
- Synthetic watermark proof.
- Invariant, fidelity, uncertainty and exploitability reports.
- Budget and exposure ledger.
- Model-risk and security review.

## Verification checklist

- [x] Deterministic reference behavior is implemented.
- [x] Synthetic origin remains explicit.
- [x] Positive promotion evidence is denied.
- [x] Runtime and execution authority are denied.
- [x] Actual MetaEditor evidence is not conflated with static validation.

## Traceability

Parent phase: [[V4_21_Robust_Optimization_And_Regret]]. Next phase: [[V4_23_Offline_Policy_Research]]. Phase map: [[00_MOC_V4_22_Generative_Path_Stress_Lab]].
