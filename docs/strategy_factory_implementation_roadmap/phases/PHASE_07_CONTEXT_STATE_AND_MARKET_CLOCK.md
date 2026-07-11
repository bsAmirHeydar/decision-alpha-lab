---
title: "Phase 07 — Context State and Market Clock"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Phase 07 — Context State and Market Clock

## Objective

Build causal, synchronized, versioned context state.

## Why This Phase Exists

This phase prevents downstream modules from inventing private assumptions. Its output becomes an explicit dependency for later phases.

## Scope

- UTC/exchange clocks
- DST
- bar synchronization
- feed freshness
- state generations
- session and cycle clock

## Required Deliverables

- `market clock service`
- `context frame`
- `freshness gates`

## Implementation Workstreams

1. **Contract and design work** — define semantics before code.
2. **Reference implementation** — implement the smallest correct behavior.
3. **Fixture construction** — create normal, boundary, and failure examples.
4. **Automated verification** — unit, contract, integration, and regression tests.
5. **Artifact production** — produce machine-readable evidence.
6. **Documentation and ADRs** — record decisions and unresolved boundaries.

## Test Requirements

- Happy-path fixture.
- Boundary-time fixture.
- Missing-input fixture.
- Duplicate or replay fixture.
- Version mismatch fixture.
- Determinism test.
- Failure-mode test.
- Integration test with the immediately preceding phase.

## Definition of Done

- [ ] Clock fixtures pass DST cases
- [ ] Cross-symbol tolerance explicit
- [ ] Stale context causes abstention
- [ ] Documentation is linked from the Master MOC.
- [ ] QA report is generated.
- [ ] Rollback path is documented.
- [ ] No phase-owned TODO remains hidden in code comments.

## Explicit Non-Goals

- Do not implement unrelated later-phase behavior.
- Do not add strategy-specific semantics to the kernel.
- Do not bypass the phase gate to accelerate a pilot.

## Recommended Commit Sequence

```text
1. docs: freeze phase semantics and ADRs
2. feat: add contracts and interfaces
3. feat: add reference implementation
4. test: add fixtures and failure cases
5. chore: add artifacts, QA, and phase report
```

## Exit Gate

The phase exits only when its deliverables are reproducible from a clean checkout and the next phase can consume them without private knowledge.
