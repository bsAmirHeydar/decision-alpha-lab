---
title: "ADR-0005 — Keep Live Order Authority Absent"
status: accepted
---

# ADR-0005 — Keep Live Order Authority Absent

## Context

The audited snapshot has market-data access but no identified order-send authority. Adding live execution before contracts, risk, replay, and paper gates would collapse the intended safety architecture.

## Decision

No live order-send capability may be added before the dedicated broker-boundary phase and its independent acceptance gate.

## Consequences

- Phase 01 may define execution schemas but not broker calls.
- Phase 17 is paper-only.
- Any unauthorized order-send call blocks the current release.
- Broker-specific code remains outside shared research modules.
