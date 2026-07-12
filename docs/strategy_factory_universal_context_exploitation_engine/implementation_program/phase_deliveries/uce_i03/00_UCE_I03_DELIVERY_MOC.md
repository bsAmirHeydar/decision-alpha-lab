---
title: "UCE-I03 — Treatment Atom Registries Delivery MOC"
tags: [ucee, treatment-atoms]
status: implemented
doc_version: 1.0.0
last_updated: 2026-07-12
---
# UCE-I03 — Treatment Atom Registries Delivery MOC


## Mission

UCE-I03 decomposes exploitation behavior into independently versioned atoms. The phase establishes six exact-version registries—entry, stop, target, trailing, management, and preliminary sizing—so a human-authored context can be evaluated through many execution styles without changing the context itself. The same contracts serve manual policies, AI search, statistical treatment comparison, Strategy Tester research, paper execution, and future live runtime compilation.

## Canonical Navigation

- [[01_SCOPE_AND_ARCHITECTURE_BOUNDARIES]]
- [[02_CANONICAL_ATOM_CONTRACT]]
- [[03_ENTRY_ATOM_REGISTRY]]
- [[04_STOP_ATOM_REGISTRY]]
- [[05_TARGET_ATOM_REGISTRY]]
- [[06_TRAILING_ATOM_REGISTRY]]
- [[07_MANAGEMENT_ATOM_REGISTRY]]
- [[08_SIZING_ATOM_REGISTRY]]
- [[09_SIDE_AWARE_PRICE_SEMANTICS]]
- [[10_PARAMETER_IDENTITY_AND_COMPATIBILITY]]
- [[11_MANUAL_AI_AND_SEARCH_PARITY]]
- [[12_CONFORMANCE_AND_GOLDEN_VECTORS]]
- [[13_RUNTIME_PERFORMANCE_AND_FAILURE_MODEL]]
- [[14_TEST_EVIDENCE_AND_ACCEPTANCE]]
- [[15_HANDOFF_TO_UCE_I04]]
- [[16_ATOM_CATALOG_REFERENCE]]
- [[17_RESEARCH_METRICS_AND_MONOTONICITY]]
- [[18_SECURITY_GOVERNANCE_AND_CHANGE_CONTROL]]

## Delivered Runtime Surface

| Registry | Canonical atoms | Responsibility |
|---|---:|---|
| Entry | 8 | Entry timing, order archetype, trigger geometry, allocation legs, expiry |
| Stop | 8 | Protective geometry, catastrophic boundaries, time invalidation |
| Target | 7 | Fixed, structural, volatility, ladder, runner, and capped-runner exits |
| Trailing | 10 | No-trail, break-even, profit lock, swing, volatility, time, and state rules |
| Management | 8 | Partials, scale-out, add-on intent, cancellation, time/session exits, guards |
| Sizing | 9 | Preliminary cash, equity, volume, tier, Kelly, volatility, drawdown, confidence, and portfolio requests |

The catalog contains 50 exact-version atoms. UCE-I03 does not compile a complete tradable treatment. That responsibility begins in UCE-I04, where compatibility, path state, and lifecycle interactions are resolved. Final commission-, spread-, slippage-, margin-, and broker-aware quantity normalization remains UCE-I05.

## Primary Code

- `mql5/Include/AlphaLab/StrategyFactory/TreatmentAtoms`
- `lab/11_strategy_factory/python/strategy_factory_treatments_v3`
- `lab/11_strategy_factory/schemas/v3/*treatment*`
- `lab/11_strategy_factory/tests/phase_uce_i03_treatments`

## Governing Rule

> A treatment atom may propose geometry, timing, management intent, or a preliminary budget. It may not mutate context truth, infer hidden economics, submit an order, or claim that independently valid atoms form a valid complete treatment.

## Upstream and Downstream

- Upstream: [[../uce_i02/00_UCE_I02_MOC|UCE-I02 Context Package SDK]]
- Program phase card: [[../../phases/UCE_I03_TREATMENT_ATOM_REGISTRIES]]
- Downstream: [[15_HANDOFF_TO_UCE_I04]]
