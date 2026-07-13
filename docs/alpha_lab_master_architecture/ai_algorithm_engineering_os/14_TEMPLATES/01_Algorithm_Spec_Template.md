---
id: AIEOS-802FACB5F3
title: "Algorithm Specification Template"
type: template
status: active
domain: template
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - template
  - template
---
# Algorithm Specification Template

> [!abstract] Purpose
> Define an implementation-independent algorithm contract.

## Usage Rules

- Copy the template into the active feature, algorithm, patch, or incident folder.
- Replace every bracketed placeholder; delete sections only with an explicit not-applicable reason.
- Link source evidence and normative notes instead of duplicating unstable content.

## Copyable Template

```markdown
# [Algorithm Name]

## Identity
- ID: [ALG-...]
- Owner: [name]
- Status: draft / approved / deprecated
- Version: [x.y.z]

## Intent and Problem
[precise problem and desired effect]

## Scope / Non-Goals
- In scope: [...]
- Out of scope: [...]

## Domain Definitions
| Term | Formal definition | Example | Counterexample |
|---|---|---|---|

## Inputs and Temporal Availability
| Input | Type/unit | Valid range | Knowledge time | Missing behavior |
|---|---|---|---|---|

## Outputs
| Output | Meaning | Consumer | Stability |
|---|---|---|---|

## State
| State item | Owner | Initial value | Mutation events | Persistence |
|---|---|---|---|---|

## Events and Transitions
| Current state | Event | Guard | Action | Next state |
|---|---|---|---|---|

## Invariants
- INV-001: [...]

## Pseudocode
```text
[...]
```

## Complexity and Budgets
[...]

## Edge Cases and Failure Semantics
[...]

## Replay / Restart / Idempotency
[...]

## Acceptance Tests and Done
[...]

## Decisions and Open Risks
[...]
```

## Completion Standard

- The artifact is understandable without the original chat.
- Normative statements are testable or explicitly marked as assumptions.
- Links, owners, versions, status, evidence, and unresolved risks are present.

## Review

Before accepting a completed instance, verify that every placeholder has been replaced, every claim points to evidence, and every unresolved item has an owner and deadline or explicit defer decision.

## Related Notes

- [[13_WORKFLOWS/_MOC|Workflows]]
- [[10_OBSIDIAN_KNOWLEDGE_SYSTEM/03_Frontmatter_Standard|Frontmatter Standard]]
