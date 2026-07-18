---
title: "Code Owner Role"
status: reference-restricted
phase_id: LCM-02
atomic_id: LCM02-033
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, atomic-concept]
---
# Code Owner Role

## Definition

`CODE_OWNER_ROLE` is a closed LCM-02 governance concept used to classify survey evidence without approving domain semantics.

## Invariant

It cannot create source-move, deletion, semantic-refactor, merge, cutover, runtime, live-order or capital authority. Missing evidence remains UNKNOWN and blocking.

## Machine representation

The concept is represented by versioned registries, immutable classification records, digests and explicit unresolved queues.

## Verification

Schema validation, closed-registry validation and hostile tests reject unknown values, authority escalation and non-canonical promotion of generated projections.

## Related

- [[00_MOC]]
- [[LCM02_PHASE_BOUNDARY]]
