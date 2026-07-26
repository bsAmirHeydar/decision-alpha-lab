---
title: Market Microstructure, Fill, Slippage and Impact Model
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- deep-design
- core-production
---

# Objective

Estimate executable outcomes for market, breakout and pullback/limit entries using bid/ask truth, order semantics, liquidity, queue uncertainty and impact.

## Capability tier

**Core Production**

# Non-negotiable principles

- Mid-price touch is not a fill.
- Market, stop and limit orders have different selection, latency and impact.
- Fill probability and conditional outcome are separate estimands for passive entry.

# Reference architecture

- Market model covers spread, latency drift, depth, volatility, size, broker execution and rejection.
- Stop model covers trigger ordering, gap-through, stop-limit semantics, spread expansion and momentum adverse selection.
- Limit model covers touch, penetration, queue proxy, volume, expiry, partial fill and post-fill adverse selection.
- Impact model separates temporary, permanent, spread, delay and opportunity costs.

# Algorithms and decision logic

- Competing-risk hazards model fill, expiry, invalidation and cancellation.
- Two-stage estimation models P(fill before expiry) and outcome conditional on fill while retaining non-fills.
- Interval-censored intrabar logic represents unknown ordering conservatively.
- Broker transport reruns exact candidates under tick size, stops level, volume step, commission, latency and rejection profiles.
- Capacity curves estimate utility degradation with size.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `ExecutionEnvironmentProfile` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `OrderIntent` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `FillHazardDataset` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `FillOutcome` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `ImpactCurve` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `BrokerTransportReport` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Fill calibration
- Partial-fill rate
- Adverse selection
- Slippage quantiles
- Trigger gap
- Impact/participation
- Missed opportunity
- Reject rate

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Limit fills from bar low without priority assumptions. |
| Failure | Stop entries get trigger price through gaps. |
| Failure | Spread is applied symmetrically. |
| Failure | Capacity is inferred without live validation. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Outcomes identify evidence resolution and uncertainty.
- [ ] Unknown ordering worsens rather than improves results.
- [ ] Execution stress can invalidate predictive edge.

# Required evidence packet

- Specification and assumption cards.
- Code, environment, data and artifact hashes.
- Positive, negative, boundary, mutation and adversarial tests.
- Baseline, ablation, stress, transport and reproducibility reports.
- Open limitations, kill criteria, downstream handoff and rollback path.

# Related architecture

- [[00_Home]]
- [[UCEE_I01_I18_Compatibility]]
- [[Anti_Overfit_Master_Protocol]]
- [[Promotion_Dossier_And_Signed_Admission]]
- [[Release_And_Production_Qualification]]
