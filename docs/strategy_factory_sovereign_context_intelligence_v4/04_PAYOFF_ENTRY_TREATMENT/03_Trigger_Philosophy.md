---
title: Trigger Philosophy
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Separate anticipatory, immediate-contextual, and confirmatory timing philosophy from the order mechanism.

## Capability tier

**Core Production**

## System design

### Anticipatory

Acts at a predeclared structural location before full confirmation and therefore requires stronger falsification and adverse-selection controls.

### Immediate contextual

Treats the context confirmation itself as sufficient and values opportunity decay explicitly.

### Confirmatory

Waits for reclaim, close, structure shift, retest, or breakout evidence and pays the resulting geometry deterioration.

### Hybrid staged trigger

Allows bounded transitions between philosophies only through a declared state machine.

## Input contracts

- `TriggerRegistry`
- `ContextKnownTime`
- `EntryMechanism`

## Output contracts

- `TriggerStateMachine`
- `ActivationEvent`
- `ExpiryEvent`

## Measurement framework

- Incremental information gained by waiting.
- Price and reward deterioration.
- Probability of missed move.
- Trigger-state transition stability.

## Adversarial questions

- Does confirmation use future bars?
- Is anticipatory entry just curve-fitted location precision?
- Can a hybrid trigger silently change philosophy?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[Path_Dependent_Treatment_State_Machines]]
