# MQL5-First Architecture

## Runtime shape

```text
MQL5 Anatomy Engine
  -> SF01_AnatomyEvent
  -> validation
  -> stable event ID
  -> JSONL/CSV artifact or in-memory runtime message
  -> later context/candidate/decision modules
```

Python receives the same event through the schema registry. It does not reconstruct event identity from a different rule. The stable-ID algorithm and canonical field ordering are mirrored byte-for-byte.

## Design rules

- No Python-only type is allowed in a canonical runtime contract.
- No dictionary ordering is relied upon for identity.
- No local-time datetime is canonical.
- No nullable field is silently overloaded; empty identifiers and explicit quality states are distinct.
- No output contract may carry a field that was unavailable at its declared known time.
- No contract can authorize order submission.
- No schema may change without semantic versioning and compatibility review.

## Fast-path implications

Phase 01 types avoid DataFrames, reflection, dynamic schema discovery, and network calls. In later phases, the decision fast path can keep these contracts in memory and update only changed fields. The current implementation uses deterministic free functions in MQL5 and immutable dataclasses in Python.

## Extension policy

New anatomy-specific fields do not go into the core event contract by default. They become versioned features in a snapshot. A core field is added only when almost every strategy needs it for identity, causality, lineage, or safety.
