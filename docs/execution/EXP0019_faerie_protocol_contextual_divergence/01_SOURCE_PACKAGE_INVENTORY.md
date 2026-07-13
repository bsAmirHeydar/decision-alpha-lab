---
title: "01 - Source Package Inventory"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 01 - Source Package Inventory

## Purpose

Establish an auditable inventory of the owner-provided Word narrative, `FP 101.mq5`, `fp101.set`, rendered pages, hashes, and derived documentation artifacts.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- The source package is evidence, not automatically the final contract.
- The owner decision response dated 2026-07-13 supersedes conflicting legacy defaults.

## Normative Invariants

1. **Every source file has a cryptographic hash.**
2. **Derived rules identify the exact source paragraph, code function, input, or owner decision that supports them.**
3. **No source file is modified by this documentation patch.**

## Deterministic Procedure

```text
Enumerate archive members.
Hash raw bytes.
Extract textual and code inventories.
Map each canonical rule to source evidence.
Record unresolved contradictions separately.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `source_path` | Exact relative or archive path. | Block traceability if absent. |
| `sha256` | Hash of raw source bytes. | Reject mismatched source. |
| `source_kind` | word, mq5, set, image, owner-response. | Reject unknown kind. |

## Edge-Case Catalogue

### Duplicate filenames

Treat path plus hash as identity; do not infer sameness from display name.

### Word/code disagreement

Owner-confirmed decisions and explicit doctrine control; preserve the legacy behavior in audit.

### Unreadable source

Mark `SOURCE_UNREADABLE`; do not fabricate a rule.

## Executable Test Obligations

1. Verify all listed hashes against files.
2. Verify each relation and input appears in inventory.
3. Verify owner-response mapping has exactly fifteen rows.

## Implementation Guidance

- Keep source audit files under `source_audit/`.
- Do not mix source evidence with generated normative contracts.


## Authority Classification

| Classification | Meaning |
|---|---|
| `OWNER_CONFIRMED` | Explicitly selected by the owner in the 15-question decision response. |
| `SOURCE_CONFIRMED` | Directly present in the original Faerie Protocol source package or owner narrative. |
| `ARCHITECTURAL_DERIVATION` | Required to make the confirmed behavior deterministic, modular, testable, or compatible with shared cores. |
| `LEGACY_OBSERVATION` | Behavior observed in `FP 101.mq5`; not automatically canonical. |
| `OPEN_DECISION` | Must not be silently hard-coded. |

Canonical priority is: `OWNER_CONFIRMED` > `SOURCE_CONFIRMED` > reviewed `ARCHITECTURAL_DERIVATION` > `LEGACY_OBSERVATION`.


## Navigation

- [[00_EXP0019_MOC|EXP0019 Master MOC]]
- [[38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
- [[33_AMBIGUITY_AND_DECISION_REGISTER|Decision Register]]
- [[40_NORMATIVE_ALGORITHM_SPECIFICATION|Normative Algorithm Specification]]
- [[44_ACCEPTANCE_GATE_FOR_CODING|Acceptance Gate for Coding]]
