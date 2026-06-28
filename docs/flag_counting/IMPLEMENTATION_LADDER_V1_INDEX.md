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
13. `11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md`
14. `12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT.md`
15. `13_LEVEL_13_VALIDATION_MATRIX.md`
16. `14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL.md`
17. `15_MODULE_INTERFACE_CONTRACTS.md`
18. `16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md`
19. `17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE.md`

## Level 11.5 implemented

`11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md` is now backed by Phoenix `FP_ExportTypes`, `FP_ExportRows`, and `FP_ExportEngine`. The layer exports canonical events, hooks, summary, and manifest CSV before renderer trust.


## Level 12 implemented

`12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT.md` is now backed by Phoenix `FP_RenderTypes`, `FP_RenderRules`, `FP_RenderAudit`, and `FP_Renderer`. Renderer emits `FP_LEVEL12`, uses canonical object names by default, and remains a read-only consumer of the canonical stream.

## Level 13 implemented

`13_LEVEL_13_VALIDATION_MATRIX.md` is now backed by Phoenix `FP_ValidationTypes`, `FP_ValidationRules`, `FP_ValidationAudit`, and `FP_ValidationEngine`. The harness emits `FP_LEVEL13`, optional `latest_validation.csv`, and validation counters in `FP_SUMMARY`.


## Level 14 release/debug/rollback layer

Phoenix now includes `FP_ReleaseTypes.mqh`, `FP_ReleaseRules.mqh`, `FP_ReleaseAudit.mqh`, and `FP_ReleaseEngine.mqh`. The active EA exposes `InpReleaseProfile` with `normal`, `clean_main`, `audit_export`, `validation`, `debug_max`, `render_off`, and `safe_rollback` profiles. Level 14 writes `latest_release.csv` and prints `FP_LEVEL14`; it does not mutate market structure.

## Level 15 module interface contracts implemented

`15_MODULE_INTERFACE_CONTRACTS.md` is now backed by Phoenix `FP_InterfaceTypes`, `FP_InterfaceRules`, `FP_InterfaceAudit`, and `FP_InterfaceEngine`. The active EA runs preflight checks after Level 14 profile overrides and postflight checks before `FP_SUMMARY`. Level 15 emits `FP_LEVEL15_PRE` and `FP_LEVEL15` and can write optional interface CSV reports.


## Level 16 patch status

Level 16 now owns the implementation-backed acceptance matrix through `FP_Acceptance*` modules. It runs after interface postflight and before final summary. It is read-only and may only report acceptance health.

## Level 17 ambiguity / final decision lock implemented

`17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE.md` is now backed by Phoenix
`FP_AmbiguityTypes`, `FP_AmbiguityRules`, `FP_AmbiguityAudit`, and
`FP_AmbiguityEngine`. The layer runs after Level 16 acceptance and before
`FP_SUMMARY`, emits `FP_LEVEL17`, and can write `latest_ambiguity.csv`.
