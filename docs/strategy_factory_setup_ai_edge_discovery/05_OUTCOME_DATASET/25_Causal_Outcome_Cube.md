---
id: SAED-E1056ED57E
title: "Causal Counterfactual Outcome Cube"
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
  - outcome
  - counterfactual
---

# Causal Counterfactual Outcome Cube

## Unit

```text
Context Occurrence × Candidate Treatment × Executable Market Path × Cost Profile
```

## Stored Outcomes

- armed/triggered/filled/expired;
- fill timestamp and price;
- partial fills;
- stop/target/trail sequence;
- MFE/MAE paths;
- gross and net R;
- spread, commission, slippage, swap and latency;
- exit reason;
- holding time and time underwater;
- missed opportunity;
- broker feasibility;
- censoring/maturity.

## Counterfactual Limits

Historical replay can compare declared candidate policies on the same market path, but it does not prove causal treatment effects when market impact or mutually exclusive orders matter. The system labels evidence as predictive/counterfactual, not randomized causal proof.
