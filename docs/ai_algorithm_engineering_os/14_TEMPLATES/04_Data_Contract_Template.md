---
id: AIEOS-4906808069
title: "Data Contract Template"
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
# Data Contract Template

> [!abstract] Purpose
> Define a versioned schema and validation contract across a boundary.

## Usage Rules

- Copy the template into the active feature, algorithm, patch, or incident folder.
- Replace every bracketed placeholder; delete sections only with an explicit not-applicable reason.
- Link source evidence and normative notes instead of duplicating unstable content.

## Copyable Template

```markdown
# [Contract Name]

- Producer: [...]
- Consumer(s): [...]
- Version: [...]
- Compatibility policy: [...]

## Schema
| Field | Type | Unit/precision | Required | Range/enum | Meaning |
|---|---|---|---|---|---|

## Ordering and Identity
[...]

## Null/Missing/Invalid Semantics
[...]

## Validation Rules
[...]

## Serialization / Transport
[...]

## Version Migration
[...]

## Contract Tests
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
