---
id: AIEOS-1B688E07CC
title: "Test Case Template"
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
# Test Case Template

> [!abstract] Purpose
> Describe one reproducible behavioral claim and its evidence.

## Usage Rules

- Copy the template into the active feature, algorithm, patch, or incident folder.
- Replace every bracketed placeholder; delete sections only with an explicit not-applicable reason.
- Link source evidence and normative notes instead of duplicating unstable content.

## Copyable Template

```markdown
# [TEST-ID] — [Name]

- Linked requirement/invariant: [...]
- Test level: unit / property / scenario / replay / visual / performance / regression
- Environment: [...]

## Initial State and Fixtures
[...]

## Input / Event Sequence
1. [...]

## Expected Intermediate State
[...]

## Expected Final Output
[...]

## Failure Signal
[...]

## Automation / Command
[...]

## Actual Result and Evidence
[...]

## Status
pass / fail / blocked / skipped
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
