---
id: AIEOS-36D92A86AE
title: "Master Feature Checklist"
type: checklist
status: active
domain: checklist
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - checklist
  - checklist
---
# Master Feature Checklist

> [!abstract] Purpose
> Control a feature from intake through durable release

## Discovery

- [ ] Problem and desired effect are observable.
- [ ] Domain terms and ambiguities are resolved or registered.
- [ ] Scope, non-goals, constraints, and failure cost are explicit.

## Design

- [ ] Entities, state, events, transitions, invariants, and edge cases are approved.
- [ ] Alternatives and complexity budgets are recorded.
- [ ] Replay, restart, idempotency, and error semantics are defined.

## Architecture

- [ ] Module boundaries, data contracts, ownership, dependencies, and compatibility are approved.
- [ ] Observability and rollback are designed.

## Implementation

- [ ] Patch identity and manifest exist.
- [ ] Change is minimal and unrelated code is untouched.
- [ ] Build succeeds and warnings are resolved or justified.

## Verification

- [ ] Requirement/invariant traceability is complete.
- [ ] Normal, edge, restart, replay, performance, visual, and regression tests pass as applicable.
- [ ] Hostile review is resolved.

## Release and Knowledge

- [ ] Archive/commit contents are reviewed.
- [ ] Rollback is tested.
- [ ] Version, changelog, docs, and vault links are updated.

## Gate Result

- **PASS:** every mandatory item is checked and evidence is linked.
- **CONDITIONAL:** only explicitly accepted, time-bounded exceptions remain.
- **FAIL:** any domain rule, safety rule, compilation rule, or state-integrity item is unresolved.

## Evidence Record

| Item | Evidence link / command output | Reviewer | Date |
|---|---|---|---|
|  |  |  |  |

## Related Notes

- [[17_GOVERNANCE/02_Quality_Gates|Quality Gates]]
- [[17_GOVERNANCE/06_Definition_of_Done|Definition of Done]]
