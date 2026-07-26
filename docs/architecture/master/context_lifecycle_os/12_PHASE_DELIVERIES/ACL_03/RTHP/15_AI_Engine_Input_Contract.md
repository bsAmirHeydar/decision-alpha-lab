# RTHP AI-Engine Input Contract

## Status

- Canonical Context: `CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1@1.0.2`
- Context lifecycle state: `CONTEXT_COMPILED`
- AI input package: `rthp.cross_symbol_cycle_divergence@1.0.0`
- Central engine modification: forbidden and unnecessary
- Real training: blocked only by unresolved external data binding

## Why this layer is separate

The semantic Context package is an approved ACL-03 source snapshot. Training integration belongs to the generated-context/plugin layer. This separation preserves semantic immutability while allowing the existing engine to consume the Context through its standard interfaces.

## Existing engine interface

RTHP implements the existing `ContextPackage` abstraction. The adapter supplies a manifest, feature descriptors, representation views, cluster rules, canonical observation mapping, and feature-frame construction. No shared SDK, compiler, trainer, dataset, validation, planner, promotion, or runtime module is changed.

## Source boundary

The adapter accepts only confirmed canonical RTHP occurrences. A source record must identify the exact Context version, event, pair, family, active and reference cycles, roles, side, polarity, time chain, data quality, reference state, source revision, content digest, and auxiliary view projection.

The adapter is not a second detector. Invalid or noncanonical records are rejected rather than repaired or guessed.

## Outputs to the engine

- immutable `ContextObservation`
- ordered `FeatureFrame`
- registered representation-view inputs
- deterministic dependence-cluster dimensions
- task references to existing shared research infrastructure
- no treatment or execution authority

## Authority ceiling

This input package may register and materialize RTHP Context observations, features, views, clusters, and research-label bindings. It may not modify Context semantics, define trade entry, submit orders, activate capital, unseal final tests, or bypass shared validation.
