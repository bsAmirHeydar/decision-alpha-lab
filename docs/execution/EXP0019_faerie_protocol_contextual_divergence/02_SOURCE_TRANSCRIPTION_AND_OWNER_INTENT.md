---
title: "02 - Source Transcription and Owner Intent"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 02 - Source Transcription and Owner Intent

## Purpose

Separate literal owner statements from architectural interpretations and legacy implementation artifacts.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- The 15-answer response is recorded verbatim in Persian as source evidence.
- Question 12 remains explicitly unanswered and cannot be promoted to owner-confirmed.

## Normative Invariants

1. **A transcription preserves meaning and paragraph order.**
2. **A paraphrase is labelled as interpretation.**
3. **Conflicts are visible and linked to decision IDs.**

## Deterministic Procedure

```text
Transcribe source.
Assign paragraph IDs.
Classify each statement.
Map to canonical rule IDs.
Attach owner-decision overrides.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `source_statement_id` | Stable paragraph or answer identifier. | Cannot cite by page alone. |
| `classification` | owner/source/legacy/derived/open. | Reject unknown classification. |
| `decision_id` | Link to frozen or open decision. | Leave null only when no decision exists. |

## Edge-Case Catalogue

### Ambiguous pronoun or window name

Preserve original text and add a separate interpretation note.

### Option letter without question context

Resolve against the archived questionnaire and record the exact option text.

### Unanswered question

Create an open decision; do not choose on behalf of owner.

## Executable Test Obligations

1. Round-trip all 15 answers to exact question text.
2. Confirm option-letter mapping.
3. Confirm Q12 remains open.

## Implementation Guidance

- Retain Persian raw transcript; all normative explanation remains English.
- Use traceability CSV for machine review.


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
