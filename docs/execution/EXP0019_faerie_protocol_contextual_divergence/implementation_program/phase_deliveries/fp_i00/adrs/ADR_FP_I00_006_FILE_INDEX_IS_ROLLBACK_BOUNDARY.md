---
title: "ADR — The File Index Is the Rollback Boundary"
tags: [exp0019, faerie-protocol, fp-i00, governance, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I00
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# The File Index Is the Rollback Boundary

## Status

Accepted for FP-I00 v1.0.0.

## Decision

Commit staging and rollback use the exact FP-I00 file index. Unrelated working-tree files are outside phase authority.

## Context

Broad `git add -A` or broad deletion makes phase evidence and rollback unsafe in a large multi-project repository.

## Consequences

- The rule is represented in policy, validator behavior, tests, and documentation.
- Violations produce a stable blocking reason code.
- Any future change requires an explicit superseding ADR and phase rebaseline.
- Downstream phases may consume the decision but may not reinterpret it.

## Rejected alternatives

- Relying on developer memory.
- Inferring authority from the absence of an order call.
- Using filenames without content hashes.
- Staging all repository changes for convenience.
- Rewriting accepted historical evidence in place.

## Verification

- Positive golden test for the accepted state.
- Negative fixture for the rejected state.
- Delivery validator checks that the ADR-linked contract remains present.
- File inventory and hash list include this ADR.

## Rollback

Remove only the files in the FP-I00 file index and restore the previously accepted implementation-program documentation. Preserve any evidence already consumed by a downstream review.

## Navigation

- [[../00_FP_I00_DELIVERY_MOC|FP-I00 Delivery MOC]]
