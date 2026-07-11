---
title: "Path Memory Is Bounded"
phase: 09
status: accepted
---
# Path Memory Is Bounded

## Decision

Path events use fixed capacity and chain hashes; overflow fails the run rather than reallocating without limit.

## Consequences

The decision is enforced through contracts, engine behavior, run manifests, replay requirements, conformance tests and promotion gates.
