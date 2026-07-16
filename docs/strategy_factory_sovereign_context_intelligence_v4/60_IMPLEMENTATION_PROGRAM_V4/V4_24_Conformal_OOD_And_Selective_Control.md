---
title: V4-24 Conformal OOD And Selective Control
status: accepted-reference
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-16'
capability_tier: research-reference
tags: [saed-v4, implementation, conformal, ood, selective-control]
---
# Phase V4-24: Conformal OOD And Selective Control

## Mission
Build a deterministic, closed-contract calibration and selective-control layer above the immutable V4-23 offline-policy research certificate. The phase converts research value estimates into finite-sample one-sided lower bounds, detects support-aware distribution shift, abstains when evidence is insufficient, reports the coverage-risk tradeoff and emits a research-only certificate plus a narrow handoff to V4-25.

## Implemented engineering slices
1. Immutable V4-23 handoff and certificate verification.
2. Decision-time, feature-known-time and outcome-observed-time separation.
3. Cluster-separated calibration, selection-validation and drift-reference roles.
4. Split conformal downside-residual calibration with finite-sample correction.
5. Mondrian regime groups with minimum-size gate and pooled fallback.
6. Robust-MAD, nearest-neighbor and support-deficit OOD ensemble.
7. Empirical OOD p-values, feature missingness gate and fail-closed semantics.
8. Multi-gate selective control preserving action masks, support and safe Skip fallback.
9. Future-outcome invariance: realized outcomes cannot affect selective decisions.
10. Frozen threshold coverage-risk frontier with cluster-bootstrap risk intervals.
11. Conservative monotone risk envelope, AURC and baseline comparison.
12. Abstention calibration maximizing coverage subject to frozen risk-upper constraints.
13. Drift diagnostics using OOD rate, PSI and mean-score ratio without runtime mutation.
14. Trial, exposure and budget ledgers; deterministic replay; model-risk and security review.
15. Static MQL5 mirror, complete Obsidian knowledge base and V4-25 handoff.

## Acceptance gates
- Unknown fields, future suffixes, protected evidence and non-finite values fail.
- Calibration, selection-validation and drift-reference clusters remain disjoint.
- One-sided conformal lower bounds use finite-sample corrected ranks.
- Tiny Mondrian groups cannot claim local coverage and use pooled fallback.
- OOD and support gates remain separate and both must pass.
- Every rejected candidate resolves to Skip with explicit reason codes.
- Realized outcomes are excluded from decision artifacts and mutation-tested.
- Coverage and selective risk are reported jointly across a frozen threshold grid.
- Drift can only trigger research abstention; it cannot mutate runtime policy.
- Baseline and UCEE authority remain intact.
- Hidden evaluation, protected exposure, runtime compilation and order submission remain zero.

## Evidence ceiling
The phase establishes a local deterministic reference implementation. It does not claim exchangeability in live markets, conditional coverage, prospective success, real alpha, promotion, runtime parity, capital authority, broker execution or production authorization. MetaEditor compilation remains `pending_local_windows`.

## Deliverables
Source modules, closed schemas, examples, golden evidence, positive/negative/mutation tests, QA tooling, MQL5 static mirrors, 240+ Obsidian notes, content-addressed certificate, inventory, file index, SHA-256 ledger and V4-25 handoff.
