---
id: AIEOS-A83CEA04D7
title: "Patch Manifest Template"
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
# Patch Manifest Template

> [!abstract] Purpose
> Control one bounded code change from intent through rollback.

## Usage Rules

- Copy the template into the active feature, algorithm, patch, or incident folder.
- Replace every bracketed placeholder; delete sections only with an explicit not-applicable reason.
- Link source evidence and normative notes instead of duplicating unstable content.

## Copyable Template

```markdown
# Patch [PATCH-ID]

## Identity
- Purpose: [...]
- Owner/reviewer: [...]
- Risk: low / medium / high / critical
- Base commit/version: [...]

## Current and Desired Behavior
[...]

## Scope
- Files to add: [...]
- Files to modify: [...]
- Files not to touch: [...]
- Non-goals: [...]

## Preserved Invariants and Contracts
[...]

## Implementation Sequence
[...]

## Verification Commands
```text
[...]
```

## Evidence and Results
[...]

## Compatibility / Migration
[...]

## Rollback
[...]

## Archive Contents / Checksum
[...]

## Commit Message
```text
[...]
```
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
