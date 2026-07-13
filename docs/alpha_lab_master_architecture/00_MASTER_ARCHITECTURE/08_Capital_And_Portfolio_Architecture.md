---
id: ALMA-508A1E7BCB
title: "Capital and Portfolio Architecture"
type: architecture
status: canonical
domain: alpha-lab-master-architecture
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - alpha-lab
  - master-architecture
---
# Capital and Portfolio Architecture

## 1. Order of Operations

```text
Support the edge
→ validate money-management policies
→ admit to portfolio
→ allocate capital
```

Money management cannot manufacture edge. Testing many sizing rules on the same return history is itself a new selection problem and requires separate validation.

## 2. Money Management Factory

Policy families may include:

- fixed cash risk;
- fixed fractional;
- stop-based maximum-loss sizing;
- volatility targeting;
- drawdown-responsive sizing;
- regime or opportunity-quality scaling;
- fractional Kelly with estimation penalty;
- risk tiers;
- portfolio-risk contribution targeting;
- equity and loss overlays.

The output is a versioned CapitalPolicy containing risk function, floors/ceilings, drawdown response, reserve requirement, stress behavior and kill conditions.

## 3. Capital Validation

Capital policies are evaluated under:

- cluster and block Monte Carlo;
- sequence and regime concentration;
- estimation error;
- tail gaps and adverse execution;
- delayed de-risking;
- parameter sensitivity;
- margin, lot step and broker constraints;
- portfolio interaction;
- time-under-water and recovery.

Selection targets robust utility, not maximum historical wealth.

## 4. Portfolio Engine

Valid strategies can still form an invalid portfolio. The portfolio layer owns:

- return and drawdown dependence;
- shared context/opportunity clusters;
- symbol, direction and factor exposure;
- simultaneous trade conflicts;
- capacity and liquidity;
- reservation ledger;
- concentration and portfolio kill limits;
- diversification value;
- strategy priority and scaling.

It may reject a valid individual trade because aggregate exposure is unacceptable.

## 5. Edge Genome

Every edge publishes a reusable profile:

- context family;
- market and horizon;
- direction and treatment style;
- return and tail shape;
- regime dependence;
- cost sensitivity;
- capacity;
- correlation and shared-event structure;
- evidence and decay state.

This allows the portfolio engine and research planner to identify duplicates, missing exposures and diversification opportunities.

## 6. Allocation Lifecycle

```text
Unallocated
→ Paper Shadow
→ Micro Allocation
→ Standard
→ Expanded
→ Reduced
→ Frozen
→ Withdrawn
```

Evidence promotion does not automatically increase capital. Allocation is independently governed and reversible.
