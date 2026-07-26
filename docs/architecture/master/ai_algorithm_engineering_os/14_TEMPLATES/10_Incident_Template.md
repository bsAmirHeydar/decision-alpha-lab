---
id: AIEOS-78C1D1847B
title: "Incident and RCA Template"
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
# Incident and RCA Template

> [!abstract] Purpose
> Document containment, root cause, correction, and prevention.

## Usage Rules

- Copy the template into the active feature, algorithm, patch, or incident folder.
- Replace every bracketed placeholder; delete sections only with an explicit not-applicable reason.
- Link source evidence and normative notes instead of duplicating unstable content.

## Copyable Template

```markdown
# Incident [INC-ID] — [Title]

## Impact and Severity
[...]

## Detection and Timeline
[...]

## Expected vs Actual Behavior
[...]

## Containment
[...]

## Evidence
[...]

## Hypotheses and Elimination
[...]

## Root Cause / Contributing Factors
[...]

## Why Controls Failed
[...]

## Corrective Patch and Verification
[...]

## Prevention Actions
| Action | Owner | Due/trigger | Evidence of completion |
|---|---|---|---|

## Closure Criteria
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
