---
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# Security and Threat Model

## Protected assets

- accepted upstream handoff and freeze digests;
- source artifact bytes and provenance;
- Setup identity uniqueness;
- blocker visibility;
- Context known-time semantics;
- Factory authority boundary;
- no-trade evidence;
- parity and handoff integrity.

## Threats and controls

### Semantic fabrication

Threat: infer rules from names, comments, static tokens, or family labels. Control: zero identities are implementation-authorized; all rule slots remain unknown and blocked; no heuristic implementation path exists.

### Authority escalation through registration

Threat: Factory registration silently makes a Setup selectable or promotable. Control: dedicated reference port, diagnostic-only visibility, four false authority fields, contract validation, bounded ACL-04 regression.

### Legacy code execution

Threat: migration adapter imports an EA or invokes terminal behavior. Control: translation-only adapter contract, `executes_legacy_source=false`, blocked adapter denial, static scan for network/process/order/chart surfaces.

### Context leakage

Threat: Setup recomputes Context using a different clock, timeframe, or threshold. Control: evaluator accepts only caller-supplied snapshots, package flags forbid independent clock and recomputation, known-time completeness is mandatory.

### Evidence suppression

Threat: no-trade, cancellation, expiry, blockers, or mismatches disappear from aggregate reports. Control: first-class decision states, blocked cases/traces, append-only blockers, non-compensatory parity, explicit closure accounting.

### Digest-cycle or publication ambiguity

Threat: manifest/receipt self-reference prevents reproducible verification. Control: manifest intentionally excludes itself and receipt; receipt binds the stable manifest; all other generated files are listed by path, size, and SHA-256.

### Source substitution

Threat: source path remains the same while bytes change. Control: source SHA-256 is frozen and retained in package, adapter, blocker, provenance, and tests. Mismatch is a hard stop.

### Restart drift

Threat: lifecycle state is reconstructed from wall time after restart. Control: digest-bound checkpoint with explicit sequence and prior decision digest; no implicit clock-based restoration.

## Residual threats

- semantic owners have not approved executable rules;
- observed legacy traces are incomplete or unavailable;
- canonical Context and Treatment identities remain unresolved for the portfolio;
- MetaEditor/MT5 validation is not available in this environment.

These are blockers, not accepted risk waivers.
