# UCEE-I04 — Complete Treatment Compiler and Causal Path State Machine

This patch implements the fourth UCEE execution phase. It composes the 50 exact-version treatment atoms from UCE-I03 into immutable treatments, validates cross-atom compatibility, compiles canonical runtime action order, replays one causal lifecycle state machine, centralizes intrabar/gap/stale policies, generates bounded treatment matrices, and preserves exact manual-treatment parity.

## Major Components

- Python `strategy_factory_treatment_compiler_v3` package.
- MQL5 `TreatmentCompiler` contracts, compiler, state machine, intrabar resolver, matrix budget, manual compiler, and conformance library.
- Twelve closed JSON schemas.
- Four golden/negative/identity vector files.
- Seventeen phase tests and cumulative I01-I04 verification.
- Thirty detailed English Obsidian documents and five ADRs.
- Status, acceptance evidence, artifact inventory, QA, manifests, hashes, and UCE-I05 handoff.

## Safety Boundary

The phase has no broker authority. Side-aware economics and capital-risk normalization are deliberately deferred to UCE-I05.
