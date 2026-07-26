---
title: Context Abstention and Fallback Ladder
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Define deterministic behavior when Context truth, support, views, models, costs, or runtime dependencies are uncertain or invalid.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Context and model health.
- Support state.
- Authority matrix.

## Output contracts

- Trade, Skip, Abstain, Manual fallback, Reject, Quarantine directive.

## Algorithmic design

- Order fallback by safety and evidence, not predicted profit.
- Separate model abstention from infrastructure failure.
- Preserve reason codes and node traces.
- Use policy-specific fallbacks: simpler model, manual policy, no-trade, or hard reject.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No fallback can bypass kill, risk, manual hard veto, admission, or portfolio constraints.
- Fallback policy is versioned and compiled.

## Measurement system

- Abstention rate.
- Selective utility.
- Fallback correctness.
- Silent failure count.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Missing view converted to zero.
- Model exception defaults trade.
- Abstention interpreted sell/buy.

## UCEE integration

- None declared.

## Required tests and evidence

- Missing dependency matrix.
- Stale context.
- OOD model output.
- Fallback parity Python/MQL5.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Abstention_And_Fallback_Master_Policy]]
- [[Manual_AI_Hybrid_Authority]]
