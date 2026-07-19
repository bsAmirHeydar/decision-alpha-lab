---
title: "LCM-03 — Canonical Identity, Alias and Locator"
status: implemented-reference
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-03
claim_ceiling: IDENTITY_AND_LOCATOR_REFERENCE_ONLY
---
# LCM-03 — Canonical Identity, Alias and Locator

LCM-03 registers path-independent provisional identities, legacy aliases, deterministic logical locators, collision blocks and a complete static consumer census over the LCM-02 active migration candidates.

## Implemented boundary

- every active candidate becomes one provisional identity candidate or one explicit ambiguity record;
- every active legacy path is registered as an alias;
- resolved include, import, documentation and configuration edges are projected into scoped alias evidence and consumer records;
- source-local functions, MQL5 inputs, experiment codes and statically recoverable chart-object prefixes are registered conservatively;
- collisions block resolution;
- physical canonical paths are not materialized;
- no source file is moved, deleted, merged, refactored, quarantined or cut over.

## Claim ceiling

`IDENTITY_AND_LOCATOR_REFERENCE_ONLY`

## Acceptance gate

All active candidates are covered by identity or explicit ambiguity; IDs are unique; aliases are deterministic or blocked; unknown versions fail closed; consumers are enumerated; object-prefix and casefold collisions are reported; source mutation is zero.

## Handoff

LCM-04 may build behavioral characterization packets and instrumentation only. It may not interpret a provisional identity as semantic approval or rewrite legacy behavior.

[[LCM03_TO_LCM04_HANDOFF_CONTRACT]]
