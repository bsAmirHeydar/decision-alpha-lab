---
title: "LCM-04 — Behavioral Characterization and Golden Traces"
status: implemented-foundation-execution-blocked
version: 2.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, characterization, golden-traces]
phase_id: LCM-04
claim_ceiling: LEGACY_BEHAVIOR_CHARACTERIZATION_ONLY
---
# LCM-04 — Behavioral Characterization and Golden Traces

LCM-04 establishes the closed characterization contract before semantic refactor. The installed reference package covers every LCM-03 identity or explicit ambiguity with a packet, static profile, required-case mapping and instrumentation plan. It also proves the trace harness through synthetic reference cases.

## Material limitation

Legacy trace execution is blocked because human semantic owners, security reviews, ambiguity resolution and MetaTrader runtime evidence are incomplete. Reference fixtures prove harness mechanics only. They are not legacy behavior or parity evidence.

## Invariants

- no source mutation, move, deletion, merge, refactor or cutover;
- observed behavior and intended correction remain separate;
- UNKNOWN is never PASS;
- drawing output is projection, not decision authority;
- dry request intent never reaches a broker;
- all identities and ambiguities have an explicit characterization disposition.

## Entry and output

Input is the exact `LCM03_TO_LCM04` handoff. Output is the content-addressed characterization package and bounded `LCM04_TO_LCM05` handoff.

## Acceptance state

`FOUNDATION_COMPLETE_LEGACY_EXECUTION_BLOCKED`

The full legacy acceptance gate remains open until owner-reviewed observed traces exist for critical paths.

## Related

- [[BEHAVIORAL_CHARACTERIZATION_HARNESS]]
- [[LCM04_PHASE_BOUNDARY]]
- [[LCM04_TRACE_SCHEMA]]
- [[LCM04_TO_LCM05_HANDOFF_CONTRACT]]
