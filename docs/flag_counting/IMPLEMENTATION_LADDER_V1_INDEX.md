# Flag Counting Implementation Ladder V1 Index

The implementation ladder is located at:

```text
docs/flag_counting/implementation_ladder_v1/
```

Start with:

```text
docs/flag_counting/implementation_ladder_v1/README.md
```

This package defines the layer-by-layer implementation plan for Phoenix Flag Counting. It is intended to stop tactical patch loops by freezing lower infrastructure before higher semantic and rendering layers are edited.

Core principle:

```text
Lower layers become audited foundations. Higher layers may depend on them but may not silently repair them.
```

Recommended reading order:

1. `00_GOVERNANCE_AND_FREEZE_PROTOCOL.md`
2. `01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE.md`
3. `02_LEVEL_02_NODE_ENGINE.md`
4. `03_LEVEL_03_NODE_IDENTITY_AND_SCALE.md`
5. `04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE.md`
6. `05_LEVEL_05_FLAG_BODY_ENGINE.md`
7. `06_LEVEL_06_INTERNAL_COUNT_ENGINE.md`
8. `07_LEVEL_07_F1_LIFECYCLE_ENGINE.md`
9. `08_LEVEL_08_F2_LIFECYCLE_ENGINE.md`
10. `09_LEVEL_09_F3_EXTENSION_AND_LOCK_ENGINE.md`
11. `10_LEVEL_10_SEQUENCE_OWNERSHIP_AND_PHASES.md`
12. `11_LEVEL_11_CANONICALIZATION_AND_AUDIT.md`
13. `12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT.md`
14. `13_LEVEL_13_VALIDATION_MATRIX.md`
15. `14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL.md`
16. `15_MODULE_INTERFACE_CONTRACTS.md`
17. `16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md`
18. `17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE.md`

## Level 11.5 implemented

`11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md` is now backed by Phoenix `FP_ExportTypes`, `FP_ExportRows`, and `FP_ExportEngine`. The layer exports canonical events, hooks, summary, and manifest CSV before renderer trust.
