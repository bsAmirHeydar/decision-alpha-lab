---
id: AIEOS-613F1EBDB7
title: "AI Context Packet Template"
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
# AI Context Packet Template

> [!abstract] Purpose
> Provide a bounded, authoritative task context to an AI role.

## Usage Rules

- Copy the template into the active feature, algorithm, patch, or incident folder.
- Replace every bracketed placeholder; delete sections only with an explicit not-applicable reason.
- Link source evidence and normative notes instead of duplicating unstable content.

## Copyable Template

```markdown
# AI Context Packet — [Task ID]

## Assigned Role and Authority
[...]

## Task / Required Output
[...]

## Authoritative Context (priority order)
1. [hard rules/spec]
2. [architecture/contracts]
3. [relevant code/files]
4. [tests/incidents/examples]

## Current Behavior
[...]

## Desired Behavior / Done
[...]

## Constraints / Non-Goals
[...]

## Files to Inspect / Modify / Not Touch
[...]

## Facts
[...]

## Assumptions / Unknowns
[...]

## Verification Commands
[...]

## Output Schema
[...]

## Stop Conditions
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
