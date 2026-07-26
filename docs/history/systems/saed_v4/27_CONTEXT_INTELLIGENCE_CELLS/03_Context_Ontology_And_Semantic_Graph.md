---
title: Context Ontology and Semantic Graph
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Represent Context anatomy, temporal order, structural relations, dependencies, contradictions, and lifecycle as an immutable semantic graph.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Canonical Context specification.
- Reference, node, phase, relationship, and view schemas.

## Output contracts

- Versioned ontology graph.
- Graph validation and contradiction report.

## Algorithmic design

- Typed nodes for occurrences, anchors, legs, references, zones, phases, symbols, sessions, and related contexts.
- Typed edges for precedes, contains, confirms, invalidates, derives-from, conflicts-with, shares-event, and depends-on.
- Temporal and structural constraints are compiled to a closed validation program.
- Unknown relations remain unknown rather than defaulting false or independent.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No learned edge may rewrite canonical doctrine.
- Learned relations are stored as hypotheses with evidence class.
- Future outcomes cannot become graph features.

## Measurement system

- Ontology coverage.
- Contradiction detection rate.
- Unknown relation rate.
- Graph stability by version.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Graph uses post-outcome nodes.
- Model-generated relation is treated canonical.
- Conflicting Contexts are silently merged.

## UCEE integration

- None declared.

## Required tests and evidence

- Topological order and temporal constraint tests.
- Contradiction injection.
- Unknown-edge preservation.
- Version migration differential test.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Context_Event_Graph_Encoder]]
- [[Bitemporal_Context_Truth_And_Suffix_Invariance]]
