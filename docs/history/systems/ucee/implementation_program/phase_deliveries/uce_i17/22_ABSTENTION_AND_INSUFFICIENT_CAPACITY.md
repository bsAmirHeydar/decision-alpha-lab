---
title: "UCE-I17 — Abstention and Insufficient Capacity"
tags: [strategy-factory, uce-i17, portfolio, capacity, risk-governance]
status: implemented_static_and_python_validated
doc_version: 1.0.0
last_updated: 2026-07-13
---
# Abstention and Insufficient Capacity

## Decision

The portfolio layer is fail-closed. A context-specific score is not comparable until promotion, prospective completion, calibration, known-time, liquidity and capacity evidence are all hash-valid. Unknown dependence is never interpreted as independence; the conservative fallback is identity-relevant and is used by both research and runtime.

## Contract and semantic owner

This chapter is governed by the closed UCE-I17 schemas and the `strategy_factory_portfolio_v3` reference package. Every behavior-changing threshold participates in canonical serialization and SHA-256 identity. Consumers may not infer missing semantics from prose, directory names or implementation defaults.

## Inputs

- Exact context package and policy versions from I16/I15.
- Promotion and calibration evidence signed by the previous gates.
- A simultaneous known-time candidate batch.
- Broker, market-hours, capacity and impact observations available at the decision cut.
- Portfolio limits, dependence fallbacks and conflict policy.

## Outputs

- Deterministically ranked opportunities with rejection reasons.
- Conservative dependence and capacity evidence.
- Hash-chained reservations and a bounded allocation plan.
- Stress, attribution, reconciliation and runtime artifacts.
- Explicit limitations and downstream handoff status.

## Invariants

1. No selected risk exists without a matching reservation.
2. Future observations cannot alter a past batch, quote, reservation or plan.
3. Unknown dependence uses a conservative fallback, never zero.
4. Hard limits, kill switch and broker constraints are vetoes, not score components.
5. Research, tester, shadow and runtime share feature, economics, treatment and risk semantics.
6. Failure, abstention, rejection and capacity degradation remain in the evidence trail.

## Failure matrix

| Failure | Required behavior | Evidence |
|---|---|---|
| Missing promotion or calibration | reject candidate | admission reason code |
| Stale or expired candidate | reject before ranking | queue audit |
| Unknown dependence | apply conservative rho | dependence source |
| Capacity or market closed | allocate zero and retain rejection | capacity quote |
| Reservation limit breach | fail closed | ledger rejection |
| Opposite symbol directions | apply explicit deny/net/hedge policy | interaction decision |
| Reconciliation mismatch | emergency de-risk and block activation | reconciliation report |
| Context-drop or correlation stress failure | validation fail | stress result |

## Required executable tests

- Canonical identity and repeated-run equality.
- Future-time and stale-candidate rejection.
- Unknown-correlation fallback.
- Reservation hard-limit and hash-chain tests.
- Capacity, spread, impact and volume-step boundaries.
- Conflicting-direction policy tests.
- Context-drop, correlation-shock and capacity-haircut stress.
- Python/MQL5 static contract parity and authority denial.

## Operator procedure

1. Freeze the simultaneous batch and all source hashes.
2. Verify promotion, calibration and context versions.
3. Rank, estimate capacity and build dependence evidence.
4. Resolve interactions and reserve risk before selection.
5. Compile the allocation plan and reconcile every reservation.
6. Run nested out-of-sample portfolio validation and stress.
7. Enter shadow only when all gates pass; retain activation blockers otherwise.
8. Archive manifests, hashes, failures, limitations and rollback data.

## Limitations and residual risk

Synthetic fixtures demonstrate contract behavior, not portfolio alpha, capacity or live safety. This repository does not currently contain two completed real prospective context promotions. Therefore I17 may validate infrastructure and deterministic semantics, but real portfolio activation remains blocked until those external evidence conditions are satisfied.

## Traceability

- Python: `lab/11_strategy_factory/python/strategy_factory_portfolio_v3/`
- Schemas: `lab/11_strategy_factory/schemas/v3/portfolio_*.schema.json`
- Tests: `lab/11_strategy_factory/tests/phase_uce_i17_portfolio/`
- MQL5: `mql5/Include/AlphaLab/StrategyFactory/Portfolio/`

