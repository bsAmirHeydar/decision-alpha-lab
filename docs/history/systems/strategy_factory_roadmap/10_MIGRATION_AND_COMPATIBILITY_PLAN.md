---
title: "Migration and Compatibility Plan"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Migration and Compatibility Plan

## Migration Strategy

1. Freeze old implementation and produce golden outputs.
2. Build adapter that emits canonical events.
3. Run old and new paths in parallel on identical data.
4. Compare event identity, known time, candidates, outcomes, and decisions.
5. Explain every mismatch.
6. Shadow the Factory output in paper mode.
7. Promote only after parity or documented intentional differences.
8. Retire duplicate old infrastructure after rollback window expires.

## Compatibility Layers

- legacy CSV import adapters;
- old event-ID mapping;
- schema translation;
- old model-artifact readers when safe;
- broker symbol alias profiles;
- migration reports.
