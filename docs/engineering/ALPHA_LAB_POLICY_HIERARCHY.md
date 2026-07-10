---
id: AIEOS2-526942447948
title: "Alpha Lab Policy Hierarchy"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab Policy Hierarchy

## Purpose

Prevent policy drift and hidden overrides. Every implementation decision must be traceable to an authority level.

## Precedence

| Rank | Authority | Examples |
|---:|---|---|
| 1 | Approved architect/domain decision | Signed specification, ADR, doctrine amendment |
| 2 | Project philosophy and immutable principles | `docs/manifesto.md`, `docs/principles.md` |
| 3 | Repository engineering policy | `AGENTS.md`, this handbook |
| 4 | Stage and experiment contracts | EXP/VAL/SIG/EXEC specifications |
| 5 | Module/data/API contracts | README, schema, interface, state-machine docs |
| 6 | Existing implementation | Current code and tests |
| 7 | AI or external recommendation | Suggestions only |

## Conflict Protocol

1. Stop implementation at the conflict boundary.
2. Cite both conflicting rules.
3. Classify the conflict as domain, architecture, interface, verification, or delivery.
4. Preserve current behavior until an authority resolves it unless safety requires fail-closed behavior.
5. Record the decision in an ADR or decision log.
6. Update downstream contracts and tests atomically.

## Normative versus Informative

- **Normative:** policy, specification, contract, ADR, hard rule, quality gate.
- **Informative:** tutorial, example, exploration, dashboard, report, model output.
- Informative artifacts cannot silently change normative behavior.

## Exception Rule

No chat message, code comment, dashboard, model score, or historical behavior becomes policy by repetition. Promotion requires explicit approval and versioning.
