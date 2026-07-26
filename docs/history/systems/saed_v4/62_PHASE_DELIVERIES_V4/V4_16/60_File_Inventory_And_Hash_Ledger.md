---
title: File Inventory and Hash Ledger
status: canonical
version: 1.0.0
phase: SAED_V4_16
created: '2026-07-16'
updated: '2026-07-16'
capability_tier: governed-challenger
tags:
  - saed-v4
  - distributional-learning
  - survival-analysis
  - tail-risk
---

# File Inventory and Hash Ledger

## Purpose

Patch file index, SHA-256 ledger, artifact inventory and delivery-manifest semantics. This note is normative for the deterministic synthetic-reference implementation and must be read together with the machine-readable contracts, frozen upstream evidence, source package, negative fixtures, QA report, claim ledger and authority boundary.

## Engineering specification

V4-16 consumes only the exact frozen V4-15 fusion champion, checkpoint registry, aligned-view identity and integrity receipt. It creates a chronologically partitioned synthetic survival dataset whose features are known at context time and whose event and outcome fields become known later. The event registry is closed: fill, stop, target, trail exit, invalidation, cancellation and expiry are mutually exclusive observed causes, while `censored` is a separate observation state and can never be rewritten as win, loss, neutral outcome or zero-return evidence.

The reference stack contains a preserved empirical/Kaplan–Meier baseline plus monotone-quantile, zero-inflated, competing-risk and tail-robust challengers. Cause-specific hazards, cumulative incidence, survival probability, quantiles, zero mass, value at risk and expected shortfall remain descriptive synthetic estimates. Calibration uses the declared chronological calibration or selection-validation role only. Quantile projection, cumulative-incidence normalization, IPCW clipping, tail effective-sample checks and deterministic hashes are explicit rather than implicit library behavior.

## Invariants and failure semantics

1. Unknown fields, unknown event causes, mutable upstream identity, future-known features, protected-evidence access, non-finite values or hash mismatch fail closed.
2. A censored path remains in the risk and censoring system; it is never coerced into an economic target.
3. Survival is bounded and non-increasing; each cause-specific cumulative incidence is bounded and non-decreasing; survival plus all cumulative incidence masses cannot exceed one.
4. Quantiles are ordered after deterministic projection. Unsupported extreme extrapolation is quarantined, and insufficient tail effective samples route to manual review.
5. Every baseline, candidate, stress run, failure and exposure is counted. No reference score signs promotion or changes policy, risk, runtime or execution state.

## Evidence and review procedure

Evidence includes closed JSON schemas, exact examples, source modules, a 240-row deterministic synthetic dataset, risk-set and IPCW ledgers, survival and distribution predictions, calibration reports, heavy-tail benchmark, best-trade removal, tail-event holdout, competing-event swap, informative-censoring sensitivity, future-suffix and fail-closed audits, immutable checkpoints, replay and integrity receipts, MQL5 static guards, Obsidian notes, file inventory and SHA-256 ledger. Reviewers should reproduce the golden bundle, mutate one invariant at a time, and confirm that the resulting directive is reject, quarantine, abstain or manual rather than silent continuation.

## Authority statement

This phase has research-reference authority only. It does not assert real outcome prediction, causality, economic uplift, real alpha, treatment ranking or selection, risk allocation, promotion, runtime eligibility, production authorization or live trading. External MetaEditor compilation, runtime parity, prospective, shadow, micro-live and live evidence remain absent.

## Related

[[00_MOC_V4_16_Distributional_Survival_And_Tail|V4-16 MOC]] · [[03_Authority_And_UCEE_Boundary|Authority]] · [[08_Censoring_Policy|Censoring]] · [[31_Tail_Calibration|Tail Calibration]] · [[56_Acceptance_Criteria|Acceptance]] · [[64_V4_17_Handoff|V4-17 Handoff]]
