---
title: "ADR — Phase Cleanliness Excludes Owned Patch Files"
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
# Phase Cleanliness Excludes Owned Patch Files

## Status

Accepted for FP-I00 v1.0.0.

## Decision

The source-control harness reports both raw cleanliness and cleanliness after excluding FP-I00-owned paths.

## Context

A newly applied patch necessarily makes the working tree dirty. The useful governance question is whether unrelated changes are also present.

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
