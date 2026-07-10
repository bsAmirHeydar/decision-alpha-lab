---
id: EXP0018-P04-BLOCKERS
title: "P04 Doctrine Blockers and Disabled Records"
type: governance-contract
status: active
project: EXP0018
phase: P04
---
# Doctrine Blockers

WW is blocked by `DY-A03` because weekly boundaries are not accepted. NP is blocked by `DY-A05` because its interpretation remains proposed. Both records remain in the canonical registry so cardinality, traceability, migration, and future activation are deterministic.

A blocked record is not absent and is not READY. It produces an explicit `BLOCKED_BY_DOCTRINE` state when configured for audit. P04 provides no runtime override that can silently bypass the blocker.
