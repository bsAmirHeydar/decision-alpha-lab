---
title: "ADR — No Holiday Calendar in FP-I03"
tags: [exp0019, faerie-protocol, fp-i03, time-calendar, obsidian]
status: normative
phase: FP-I03
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# No Holiday Calendar in FP-I03

## Status

Accepted.

## Decision

FP-I03 defines structural recurring intervals only.

## Rationale

Holiday and early-close behavior requires a separate versioned market-calendar authority and is not inferred.

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
