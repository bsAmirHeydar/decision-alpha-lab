---
id: AIEOS2-8FFAF774224C
title: "Alpha Lab Execution Safety Standard"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab Execution Safety Standard

## Capital Boundary

Research, ranking, model, and dashboard outputs have zero execution authority by default. Only versioned production decision contracts may reach execution.

## Required Layers

```text
approved decision signal
→ execution intent
→ risk authorization
→ broker adapter
→ order state machine
→ reconciliation
→ monitoring/kill switch
```

## Safety Requirements

- Paper mode precedes live mode.
- Fixed magic/strategy identity and deterministic position IDs.
- Idempotent retries; duplicate order prevention.
- Explicit market/session/spread/slippage/volume checks.
- Maximum risk and exposure enforced outside the model.
- Broker position/order state reconciled with internal state.
- Startup recovery and partial-fill behavior specified.
- Fail closed on stale data, clock uncertainty, invalid symbol, missing stop, or corrupted state.
- Emergency disable and rollback are tested.

## Separation

The model may score or rank. The risk engine sizes within approved bounds. The execution engine sends approved intents. No layer may silently absorb another layer’s authority.
