---
id: AIEOS-6D60A42D07
title: "Module README Template"
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
# Module README Template

> [!abstract] Purpose
> Describe a code or documentation module and its contracts.

## Usage Rules

- Copy the template into the active feature, algorithm, patch, or incident folder.
- Replace every bracketed placeholder; delete sections only with an explicit not-applicable reason.
- Link source evidence and normative notes instead of duplicating unstable content.

## Copyable Template

```markdown
# [Module Name]

## Responsibility
[...]

## Non-Responsibilities
[...]

## Public Interface
[...]

## State Ownership
[...]

## Dependencies / Consumers
[...]

## Data and Error Contracts
[...]

## Lifecycle
[...]

## Performance Budget
[...]

## Testing
[...]

## Known Risks / Extension Points
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
