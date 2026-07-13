---
id: AIEOS-967A52278F
title: "State Machine Template"
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
# State Machine Template

> [!abstract] Purpose
> Specify lifecycle states, legal transitions, guards, actions, and invariants.

## Usage Rules

- Copy the template into the active feature, algorithm, patch, or incident folder.
- Replace every bracketed placeholder; delete sections only with an explicit not-applicable reason.
- Link source evidence and normative notes instead of duplicating unstable content.

## Copyable Template

```markdown
# [State Machine Name]

## Purpose and Entity
[...]

## States
| State | Meaning | Entry conditions | Exit conditions | Terminal? |
|---|---|---|---|---|

## Events
| Event | Source | Payload | Ordering/dedup rule |
|---|---|---|---|

## Transition Table
| From | Event | Guard | Actions | To | Error behavior |
|---|---|---|---|---|---|

## Invariants
[...]

## Illegal Transitions
[...]

## Restart/Reconstruction
[...]

## Transition Tests
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
