---
title: EXP0018 P10 Temporal Visuals Do Not Require A Paired Divergence Source
tags:
  - exp0018
  - phase10
  - visual-anatomy
  - broker-symbols
  - resilience
status: implemented
---

# EXP0018 P10 Temporal Visuals Do Not Require A Paired Divergence Source

Daily frames, A/L/N/P Sessions, a1–p4 subcycles, 22.5-minute micro-quarter boundaries, the 17:00–18:00 gap, TDO, and TWO are symbol-local temporal projections. They must remain available on the attached chart when the SPX/NDX paired divergence pipeline is unavailable.

The paired source remains mandatory only for divergence evidence and Hunter-side divergence lines.

## Consequences

- Broker alias failure cannot remove all temporal drawings.
- The attached chart can render from its own validated closed bars.
- `No paired source` is a degraded capability state, not an Expert initialization failure.
- Local fallback never produces hunt or divergence facts.

## Related

- [[CG_EXP0018_PHASE10_UNIFIED_VISUAL_ANATOMY_MOC]]
- [[EXP0018_P02_No_Data_Is_Not_No_Hunt]]
- [[EXP0018_P08_Renderer_Is_A_Projection]]
