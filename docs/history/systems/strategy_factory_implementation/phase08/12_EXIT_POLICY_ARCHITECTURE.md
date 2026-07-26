---
title: "Exit Policy Architecture"
phase: 08
status: canonical
---
# Exit Policy Architecture

Exit plans may be price-target, time-only, price-or-time or structural. Phase 08 stores the intended resolution geometry but does not simulate it. Partial fractions are represented but multi-stage lifecycle behavior is deferred to the outcome engine. Exit policies must not inspect future path data.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
