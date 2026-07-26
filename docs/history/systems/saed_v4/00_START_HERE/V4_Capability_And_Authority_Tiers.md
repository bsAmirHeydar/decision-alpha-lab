---
title: V4 Capability and Authority Tiers
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
  - authority
  - tiers
---

# Capability and authority tiers

| Tier | Meaning | Permitted examples | Live authority |
|---|---|---|---|
| C0 | Deterministic core | schemas, replay, baseline, constraints | none |
| C1 | Governed production candidate | calibrated linear/tree/rank/survival models | only after UCEE admission |
| C2 | Governed challenger | deep sequence, graph, multimodal, foundation adapter | none before promotion |
| C3 | Research-only | world models, diffusion/flow, offline RL, causal discovery | prohibited |
| C4 | Prohibited-to-live | unrestricted agents, free-form actions, self-modifying risk | permanently prohibited |

No algorithm migrates between tiers by implementation convenience. Migration requires a new ADR, model-risk review, evidence dossier and runtime qualification.
