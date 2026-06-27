# Flag Counting Documentation

This folder contains the authoritative design documents for the Flag Counting engine.

## Documents

- `FLAG_COUNTING_CONCEPT_SPEC_V3.md` — full conceptual contract.
- `FLAG_COUNTING_ALGORITHM_BLUEPRINT.md` — implementation-level algorithms and data models.
- `FLAG_COUNTING_GLOSSARY.md` — definitions of all terms used by the engine.

## Current implementation policy

Do not keep patching the old loose scanner as the final engine. The final implementation must be derived from the v3 specification:

- fractal multi-scale node streams
- parallel sequences
- F1/F2/F3 parent-child grammar
- ND/Hook partitioning
- queryable state API
- audit/replay support
- clean body-only renderer

## Minimum production target

The final engine must be able to answer from code:

- Are we in ND or F phase?
- Which F-level is active?
- What is the current direction?
- What scale and sequence own the current movement?
- What is the invalidation boundary?
- What is the next expected event?
