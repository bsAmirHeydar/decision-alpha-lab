---
id: SAED-DD7715C040
title: "Master Architecture — Contextual Treatment Discovery"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - master-architecture
---

# Master Architecture — Contextual Treatment Discovery

## 1. Architectural Position

This module is **Phase C productization** on top of the completed UCEE kernel. It does not fork or replace the existing Context, Treatment, Dataset, Trainer, Experiment, Promotion, Policy, Runtime, Portfolio, or Production contracts. It composes them into a domain-specific Setup Discovery product.

## 2. Central Question

For a valid Context occurrence available at decision time:

> Which compatible complete Treatment has the highest reliable, cost-adjusted and risk-constrained utility — or should the correct action be Skip/Abstain?

The system is not optimized to maximize historical profit. It is optimized to discover **reproducible conditional economic value** while controlling false discovery.

## 3. Four-Layer Separation

### Semantic Layer

Owned by the Context engine. It defines what happened, direction, lifecycle, known time, freshness, required views, and invalidation semantics.

### Action Layer

Owned by the Treatment Factory. It defines all permissible entry, stop, exit, management and risk-request atoms and compiles only coherent complete bundles.

### Learning Layer

Owned by Trainer/Experiment systems. It estimates eligibility, fill, outcomes, ranking, treatment choice, uncertainty, novelty and regime routing without access to forbidden future information.

### Authority Layer

Owned by Promotion, Policy, Runtime, Risk and Portfolio. A trained model has no execution authority. It becomes deployable only through signed evidence and a bounded policy graph.

## 4. Architectural Invariants

1. Context identity and Treatment identity are separate.
2. Every model candidate is compared with Manual, Always-Trade, Never-Trade and simple unconditional baselines.
3. `Skip` is a first-class candidate.
4. Every candidate sibling from one opportunity remains in the same fold/cluster.
5. All considered, pruned, failed, timed-out and cancelled trials remain in the selection universe.
6. Locked final-test outcomes cannot influence search, prompting, feature design, thresholds or model selection.
7. Path-dependent policies require replay at sufficient temporal resolution.
8. Wide-stop high-hit policies must satisfy minimum net reward and tail/capital constraints.
9. Convex policies are not judged by win rate alone.
10. Confidence cannot directly set leverage.
11. Unknown support, stale Context, missing views or excessive cost lead to abstention/fallback.
12. No model may create undeclared order types, Treatment atoms or broker behavior.

## 5. Major Subsystems

| Subsystem | Responsibility | UCEE foundation |
|---|---|---|
| Style Registry | payoff, entry, trigger and objective taxonomy | I03/I04 |
| Treatment Universe Compiler | compatible complete candidates | I03/I04 |
| Outcome Cube | side-aware executable counterfactuals | I05/I06 |
| Dataset Factory | clustered causal rows and folds | I06 |
| Trainer Task Graph | multi-task learning and OOF predictions | I07–I10 |
| Experiment Governance | DAG, search budgets, ledgers | I11 |
| Statistical Promotion | anti-overfit and veto gates | I12 |
| Policy Compiler | manual/AI/hybrid/abstention/fallback | I13 |
| Runtime Handoff | immutable preprocessing/model parity | I14 |
| Context Tournament | frozen real-context evaluation | I15 |
| Onboarding | repeatable use across Context families | I16 |
| Portfolio | shared allocation and capacity | I17 |
| Production | compile, shadow, authorization, recovery | I18 |

## 6. End State

A new Context should require only:

```text
Context Specification
+ Compatibility Declarations
+ Candidate Style Registry
+ Objective Profile
+ Falsification Plan
```

Everything downstream is reused and produces a signed, reproducible promotion or rejection dossier.
