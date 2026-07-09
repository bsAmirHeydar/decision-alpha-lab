# Exp0017 Forbidden Assumptions En

This document lists all assumptions forbidden before statistical testing: CG superiority, symbol superiority, direction superiority, time-window superiority, overlap superiority, stop-size filtering, late-entry filtering, emotional signal quality, and AI strategy mutation.

## Canonical Current-Version Boundaries

- The robot must learn to see before it is allowed to decide.
- The current version is statistical-only and doctrine-preserving.
- All confirmed tradeable signals should be recorded before ranking or filtering.
- AI may explain, rank, compare, and warn, but it cannot mutate the strategy.
- Future optimization is allowed only through a separate version gate.

## Required Traceability

Every implemented module must expose the state it creates: time field, cycle group, reference candidate, hunt state, divergence state, confirmation state, invalidation state, signal record, and statistical result.
