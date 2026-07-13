---
id: AIEOS-F0C37A6A07
title: "AI Output Acceptance Checklist"
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
# AI Output Acceptance Checklist

> [!abstract] Purpose
> Decide whether an AI-generated artifact may enter the project

## Grounding

- [ ] Repository-specific claims come from inspected files or tool output.
- [ ] Facts, assumptions, unknowns, and recommendations are separated.

## Scope

- [ ] Output follows the assigned role and does not expand scope silently.

## Engineering

- [ ] Domain rules, invariants, architecture, conventions, compatibility, and security are preserved.

## Evidence

- [ ] Commands were actually run or explicitly marked unrun.
- [ ] Tests and review results are attached.

## Understanding

- [ ] A human maintainer can explain and own the result.

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
