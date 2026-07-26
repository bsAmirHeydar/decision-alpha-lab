---
id: AIEOS-39894D97B0
title: "Code Readiness Checklist"
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
# Code Readiness Checklist

> [!abstract] Purpose
> Decide whether a design may enter code

## Inputs

- [ ] Approved spec, architecture contracts, context packet, patch manifest, and relevant files are available.

## Scope

- [ ] Files to touch, files not to touch, non-goals, compatibility, and rollback are explicit.

## Tests

- [ ] Failing/characterization tests or clear acceptance tests exist before implementation.

## Agent Control

- [ ] AI role, authority, output schema, verification commands, and stop conditions are explicit.

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
