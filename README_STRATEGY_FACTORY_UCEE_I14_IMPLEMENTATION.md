# Strategy Factory UCE-I14 — Immutable Runtime Compilation

UCE-I14 binds the exact accepted UCE-I13 policy generation into one immutable runtime bundle. The implementation provides closed component identity, deterministic preprocessing, approved-native export, optional ONNX capability probing, source/export/MQL5 parity certification, bounded runtime hosting, atomic generation activation, restart-safe decision journaling, failure qualification, and exact rollback.

## Delivered surfaces

- `strategy_factory_runtime_v3`: 24 Python modules.
- `runtime_*.schema.json`: 25 closed schemas.
- `examples/uce_i14`: complete golden bundle, model, export, parity, failure, activation, requests, decisions, evidence, capabilities, and rollback fixtures.
- `ImmutableRuntime`: 12 MQL5 include contracts plus four diagnostic/self-test experts.
- `phase_uce_i14_runtime_compilation`: contract, preprocessing, export, parity, bundle, signature, generation, host, journal, replay, failure, CLI, migration, schema, and boundary tests.
- 38 detailed implementation chapters and 10 atomic Obsidian concepts.

## Safety boundary

The runtime host returns bounded decisions only. `order_authority` is structurally forbidden, generic Python and MQL5 runtime surfaces contain no broker or network calls, and live mode requires a separately authorized isolated adapter.

## Export qualification

The approved-native canonical representation is fully executable in this environment. ONNX and ONNX Runtime are probed explicitly. When unavailable or when no project-specific converter is registered, ONNX export fails closed and no parity claim is issued.

## Validation

Run `tools/strategy_factory/run_uce_i14_tests.ps1`. Real MetaEditor compilation remains a local Windows gate and must not be inferred from static checks.
