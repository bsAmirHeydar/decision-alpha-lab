---
title: "ADR-0004 — Select CP0001/M0001 as Local Foundation Pilot"
status: accepted
---

# ADR-0004 — Select CP0001/M0001 as Local Foundation Pilot

## Context

The broader roadmap names EXP0017 and NDS as pilots, but the uploaded repository snapshot contains neither. It does contain a working structural-node and metric path.

## Decision

Use CP0001 Structural Nodes + M0001 RTV as the local foundation compatibility pilot through early implementation phases. Preserve EXP0017 and NDS as later full-platform pilots once their code is present.

## Consequences

- Early contracts can be tested against real existing code.
- The pilot proves data/anatomy/feature/artifact compatibility, not profitability.
- Phase 20 and 21 remain blocked on receipt of the current full repository.
