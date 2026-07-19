---
title: "LCM-05 Handoff Contract"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-04, characterization]
phase_id: LCM-04
claim_ceiling: LEGACY_BEHAVIOR_CHARACTERIZATION_ONLY
---
# LCM-05 Handoff Contract

## Contract

This control belongs to LCM-04 and is bound to the exact LCM-03 identity handoff. It may describe, register, profile, instrument by plan and compare traces. It may not mutate legacy semantics, move or delete sources, merge identities, cut over consumers, submit orders or activate capital.

## Required evidence

Evidence must be content-addressed, replayable, known-time explicit and classified as either reference fixture or legacy observed. Reference fixture evidence cannot satisfy a legacy parity gate. Missing owner or runtime evidence remains `UNKNOWN` or blocked.

## Verification

The machine package binds this contract through packet indexes, static profiles, closed case registries, normalized traces, known-time audit, event ledger, provenance, receipt and output manifest.

## Related

- [[LCM_04_BEHAVIORAL_CHARACTERIZATION_AND_GOLDEN_TRACES]]
- [[00_MOC]]
