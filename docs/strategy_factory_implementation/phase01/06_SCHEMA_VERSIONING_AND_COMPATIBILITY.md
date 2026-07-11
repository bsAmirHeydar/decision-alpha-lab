# Schema Versioning and Compatibility

## Semantic version

Each schema has `major.minor.patch`.

- Major: incompatible field meaning, identity, type, or required-field change.
- Minor: backward-compatible optional field or capability addition.
- Patch: validation clarification or bug fix that does not alter valid payload meaning.

## Compatibility rule

Producer and consumer must share namespace, schema name, and major version. A consumer can read an equal or older producer minor version. A newer producer minor may require an explicit migration adapter. A major mismatch is rejected.

## Registry

The machine-readable registry under `lab/11_strategy_factory/schemas/v1/contract_registry.json` records the canonical schema name, MQL5 header, Python mirror type, required fields, authority model, and version.

## Change protocol

1. Open ADR.
2. Add new test vectors.
3. Update MQL5 first.
4. Update schema registry and JSON Schema.
5. Update Python mirror.
6. Run cross-language tests.
7. Add migration reader if needed.
8. Never rewrite historical artifacts in place.
