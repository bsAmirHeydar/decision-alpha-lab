---
title: "Duplicate Declaration"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-05, atomic-concept]
phase_id: LCM-05
claim_ceiling: TARGET_TOPOLOGY_REFERENCE_ONLY
---
# Duplicate Declaration

`Duplicate Declaration` is an atomic LCM-05 concept. Its meaning is fixed by the closed target-topology registries and the topology package. It cannot be used to infer owner approval, semantic equivalence, behavioral parity, path materialization, cutover or execution authority.

## Invariant

The concept is deterministic, content-addressed where persistent, root-relative where path-bearing, and fail-closed when evidence is missing.

## Related

- [[00_MOC]]
- [[LCM_05_TARGET_TOPOLOGY_AND_REPOSITORY_LOCATOR_MIGRATION]]
