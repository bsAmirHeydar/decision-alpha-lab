---
id: SAED-34F24BBD52
title: "Trail Replay and Path Reconstruction"
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
  - trailing
---

# Trail Replay and Path Reconstruction

## Why Endpoint Labels Fail

For trailing exits, two paths with identical final high/low can produce different exits. The replay must know the ordered sequence of activation, ratchet, pullback and exit.

## Resolution Policy

- Prefer tick or event-level replay.
- If unavailable, use lower-timeframe bars with frozen pessimistic ordering.
- Mark ambiguous cases and quantify sensitivity.
- Never choose intrabar ordering after seeing which result is better.

## Derived Metrics

- capture ratio = realized favorable move / maximum favorable move;
- giveback from peak;
- premature-exit rate;
- post-exit continuation;
- trail update count;
- activation delay;
- path smoothness and chop cohorts.
