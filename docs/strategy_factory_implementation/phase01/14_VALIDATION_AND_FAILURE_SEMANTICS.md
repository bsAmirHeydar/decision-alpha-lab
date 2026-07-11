# Validation and Failure Semantics

Contracts fail closed. Invalid data is not repaired inside the canonical type.

## Validation layers

1. Primitive validation: finite numbers, safe identifiers, time range.
2. Structural validation: required fields and tagged types.
3. Causal validation: known time does not exceed snapshot or confirmation.
4. Identity validation: supplied stable ID equals derived ID.
5. Compatibility validation: schema key and major version accepted.
6. Domain validation: owned by later adapters and policies.

## Failure outputs

MQL5 validators return `false` with a precise error string. Python raises `ContractValidationError`. Runtime callers must convert failure into abstention, quarantine, or test failure—not a partially valid event.

## Quarantine

Later ingestion modules should write rejected payloads to a versioned quarantine artifact with reason, producer, source hash, and raw line. They must not contaminate training datasets.
