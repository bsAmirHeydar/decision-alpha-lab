---
id: AIEOS-4D78C3EED4
title: "Architecture Decision Record Template"
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
# Architecture Decision Record Template

> [!abstract] Purpose
> Record a significant decision, alternatives, rationale, and consequences.

## Usage Rules

- Copy the template into the active feature, algorithm, patch, or incident folder.
- Replace every bracketed placeholder; delete sections only with an explicit not-applicable reason.
- Link source evidence and normative notes instead of duplicating unstable content.

## Copyable Template

```markdown
# ADR-[NNNN] — [Decision]

- Status: proposed / accepted / superseded / rejected
- Date: [...]
- Decision owners: [...]

## Context
[...]

## Decision Drivers
[...]

## Options Considered
### Option A
[...]
### Option B
[...]

## Decision
[...]

## Evidence and Rationale
[...]

## Consequences
- Positive: [...]
- Negative: [...]
- Risks: [...]

## Verification and Revisit Trigger
[...]

## Supersedes / Superseded By
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
