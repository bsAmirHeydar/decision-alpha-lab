---
title: "LCM-07 — Shared Engine Extraction"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-07
claim_ceiling: SHARED_ENGINE_EXTRACTION_REFERENCE_ONLY
---
# LCM-07 — Shared Engine Extraction

## Decision

LCM-07 implements deterministic shared-engine candidate discovery, exact normalized-body clustering, variance catalogs, static equivalence evidence, parameterized design proposals, consumer adapter proposals and governance records. It does not materialize a shared engine or mutate any legacy source.

## Architecture

```text
LCM06_TO_LCM07
  → upstream integrity gateway
  → authority permit
  → protected-platform exclusion
  → MQL function inventory
  → exact normalized-body candidate clusters
  → variance catalog
  → non-compensatory equivalence gates
  → parameterized design proposals
  → consumer adapter proposals
  → governance and extraction decisions
  → atomic publication
  → LCM07_TO_LCM08
```

## Acceptance

`REFERENCE_DISCOVERY_ACCEPTED_EXTRACTION_BLOCKED_PENDING_RUNTIME_AND_OWNER_APPROVAL`

## Hard boundary

Static source equivalence is evidence only. Named ownership, independent review, MetaEditor compilation, runtime parity, consumer regression, restart parity and rollback rehearsal remain mandatory before extraction or cutover.
