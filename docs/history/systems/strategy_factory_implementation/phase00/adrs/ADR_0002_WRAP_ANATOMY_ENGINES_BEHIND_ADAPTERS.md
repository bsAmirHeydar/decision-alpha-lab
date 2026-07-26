---
title: "ADR-0002 — Wrap Anatomy Engines Behind Adapters"
status: accepted
---

# ADR-0002 — Wrap Anatomy Engines Behind Adapters

## Context

The existing L-rule detector contains market meaning. Future NDS, SMT, Daye, ICT, and Astro engines will contain different meanings. Moving them into shared core code would make the kernel a strategy monolith.

## Decision

Preserve anatomy implementations behind versioned adapters that emit canonical events and features. The kernel owns transport and lifecycle contracts, not the definition of a valid anatomy.

## Consequences

- Legacy behavior can be differential-tested.
- Strategy semantics remain independently versioned.
- New anatomy programs do not require a new research pipeline.
- Adapter boundaries become mandatory integration points.
