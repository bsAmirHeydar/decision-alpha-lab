---
title: "ADR — Ambiguous Local Time Requires Policy"
tags: [exp0019, faerie-protocol, fp-i03, time-calendar, obsidian]
status: normative
phase: FP-I03
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Ambiguous Local Time Requires Policy

## Status

Accepted.

## Decision

Repeated fall-back local times expose both UTC candidates and require REJECT/EARLIEST/LATEST.

## Rationale

Selecting implicitly would make construction dependent on library defaults.

## Consequences

- The rule is included in semantic configuration or registry identity.
- Python and MQL5 mirrors must produce compatible boundary facts.
- Golden fixtures and negative tests enforce the decision.
- A change requires a new version and downstream rebaseline.

## Rejected alternatives

- Inferring behavior from broker or chart state.
- Using inclusive end boundaries.
- Repairing ambiguous or missing civil values silently.
- Treating documented time rules as projection-only settings.

## Verification

- Unit and boundary tests.
- Golden vector hash.
- MQL5 static/self-test evidence.
- Delivery validator and exact file inventory.

## Navigation

- [[../00_FP_I03_DELIVERY_MOC|FP-I03 Delivery MOC]]
