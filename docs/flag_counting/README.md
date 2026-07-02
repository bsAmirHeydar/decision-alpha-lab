# Flag Counting Documentation

## Active source of truth

Start here:

```text
docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
```

That file is the final decision source for Phoenix. If any older Flag Counting document conflicts with it, the current canon wins.

## Active implementation

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
mql5/Include/FlagCountingPhoenix/
```

Phoenix is the only active implementation path.

## Active canonical documents

Read in this order:

1. `FLAG_COUNTING_CURRENT_CANON.md` — final decisions and conflict resolver.
2. `FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md` — semantic F1/F2/F3 and Hook/ND contract.
3. `FLAG_COUNTING_ENGINEERING_PACK_V5.md` — engineering package index.
4. `engineering_pack_v5/` — definitions, explanations, algorithms, visualization contracts.
5. `implementation_ladder_v1/` — implementation order, interfaces, freeze gates, validation, audit/export.
6. `phoenix_rebuild/` — Phoenix-specific repair notes, subordinate to the current canon.

## Legacy/history documents

The following files remain useful as historical context, but must not be used as the decision source for new Phoenix code:

```text
FLAG_COUNTING_CONCEPT_SPEC_V2.md
FLAG_COUNTING_CONCEPT_SPEC_V3.md
FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md
FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md
FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md
FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md
FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md
FLAG_COUNTING_STATE_MACHINE_V2.md
FLAG_COUNTING_STATE_MACHINE_V3.md
FLAG_COUNTING_STATE_MACHINE_V4.md
FLAG_COUNTING_VNEXT_IMPLEMENTATION.md
FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md
```

M0007, VNext, and V6 are archived/reference implementations only.

## Non-negotiable rule

Flag Counting is a high/low-only, L-node-based, stateful sequence engine:

```text
ND/Hook -> F1 -> F2 -> F3 -> Extension/Lock
```

It is not a sliding-window pattern scanner, and the renderer is never allowed to invent or repair structure logic.

## Phoenix Level 11.5 raw audit export

Phoenix now includes a read-only raw audit export layer before renderer trust. Enable it from `FlagCountingPhoenixExperiment.mq5` with:

```text
InpExportAuditFiles = true
```

Default output goes to:

```text
MQL5/Files/FlagCountingPhoenix/latest_events.csv
MQL5/Files/FlagCountingPhoenix/latest_hooks.csv
MQL5/Files/FlagCountingPhoenix/latest_summary.csv
MQL5/Files/FlagCountingPhoenix/latest_manifest.csv
```

This export serializes the Level 11 canonical stream. It does not create, hide, repair, or draw structures.


## Level 12 renderer

Renderer now uses `FP_RenderTypes`, `FP_RenderRules`, `FP_RenderAudit`, and `FP_Renderer`. It draws after Level 11.5 export, uses canonical object names by default, emits `FP_LEVEL12`, and does not mutate logical events or hooks.

## Phoenix Level 13 validation

Level 13 is implemented as a read-only validation harness. Enable it in MT5 with:

```text
InpValidationEnabled = true
```

Baseline mode is the default and writes `latest_validation.csv` with actual counts and `baseline_required` warnings for unset expected ranges. Regression mode is created by filling the expected min/max inputs for the pinned validation case.


## Level 14 release/debug/rollback layer

Phoenix now includes `FP_ReleaseTypes.mqh`, `FP_ReleaseRules.mqh`, `FP_ReleaseAudit.mqh`, and `FP_ReleaseEngine.mqh`. The active EA exposes `InpReleaseProfile` with `normal`, `clean_main`, `audit_export`, `validation`, `debug_max`, `render_off`, and `safe_rollback` profiles. Level 14 writes `latest_release.csv` and prints `FP_LEVEL14`; it does not mutate market structure.

## Level 15 module interface contracts

Phoenix now includes `FP_InterfaceTypes.mqh`, `FP_InterfaceRules.mqh`, `FP_InterfaceAudit.mqh`, and `FP_InterfaceEngine.mqh`. Level 15 runs read-only preflight and postflight interface checks, emits `FP_LEVEL15_PRE` and `FP_LEVEL15`, and can optionally write `latest_interface_pre.csv` / `latest_interface_post.csv`. It verifies module boundary health without mutating market structures or renderer output.


## Level 16 acceptance matrix

Phoenix now includes `FP_AcceptanceTypes.mqh`, `FP_AcceptanceRules.mqh`, `FP_AcceptanceAudit.mqh`, and `FP_AcceptanceEngine.mqh`. Level 16 runs after Level 15 postflight and before `FP_SUMMARY`, emits `FP_LEVEL16`, and can optionally write `latest_acceptance.csv`. It is a read-only runbook gate: it aggregates timebase, node, hook, body, internal-count, F1/F2/F3 lifecycle, ownership, canonicalization, export, renderer, validation, release, and interface health into one acceptance matrix.

## Level 17 decision lock

Phoenix Level 17 closes the old ambiguity list. It runs a read-only runtime
check after the acceptance matrix and verifies that current inputs/reports match
`FLAG_COUNTING_CURRENT_CANON.md`. It emits `FP_LEVEL17` and can write
`latest_ambiguity.csv`.


## Level 18 static QA

Phoenix now has a final compile/static QA hardening pass. Runtime emits `FP_LEVEL18`; source-side scanning is available with:

```powershell
python tools/flag_counting/static_qa.py --root . --csv reports/flag_counting_static_qa.csv
```


## Level 19 — Clean Isolated State Gate

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md
```

Clean rebuild of Level 19 as a read-only State Gate. It exports `latest_state_gate_level19.csv`, keeps the panel disabled by default, uses a dedicated panel prefix when enabled, and does not touch renderer files, F/Hook/Node drawings, curves, lines, or prior market-anatomy logic.


## Level 19A — Silent Defaults and Lifecycle Cleanup

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_19A_SILENT_DEFAULTS_AND_LIFECYCLE_CLEANUP.md
```

Level 19A disables all print inputs by default while keeping them manually switchable, and makes chart-object cleanup explicit on init, deinit, timeframe change, remove, recompile, parameter change, and template apply without touching renderer source files or F/Hook/Node drawing logic.


## Level 19B — Closed-Bar State Ledger

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_19B_CLOSED_BAR_STATE_LEDGER.md
```

Level 19B adds an append-only closed-bar state ledger CSV while preserving the clean read-only Level 19 contract. It keeps the panel disabled by default, prints silent by default, and does not touch renderer source files, curves, F/Hook/Node drawings, RTV, zones, or execution logic.


## Level 19C — Closed-Bar State Delta Ledger

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_19C_STATE_DELTA_LEDGER.md
```

Level 19C adds `state_gate_level19_state_delta.csv`, comparing each newly observed closed-bar State Gate snapshot against the previous one. It records structural deltas for event counts, Hook counts, F1/F2/F3 counts, ND counts, latest visible event/hook changes, render status changes, validation status changes, and state-key changes without touching renderer source files, chart curves, F/Hook/Node drawings, or execution logic.


## Level 19D — Closed-Bar Transition Event Ledger

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_19D_TRANSITION_EVENT_LEDGER.md
```

Level 19D adds `state_gate_level19_transition_events.csv`, classifying each closed-bar state delta into transition families and severities such as F1/F2/F3 expansion, F-count contraction, Hook count change, ND count change, visibility change, health change, and no-change. It remains read-only, panel-off by default, print-silent by default, and does not touch renderer source files, chart curves, F/Hook/Node drawings, RTV, zones, or execution logic.


## Level 19Z — Complete Observation Suite

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE.md
```

Level 19Z completes the clean Level 19 observation layer. It adds transition summary, transition stability, regime labels, and completion status outputs while preserving the no-touch renderer contract, keeping the panel disabled by default, keeping prints disabled by default, and avoiding entry, paper trading, broker requests, and real execution.


## Level 20 — Entry Bridge / X-Y Anchor Join

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN.md
```

Level 20 adds `state_gate_level20_entry_bridge.csv`, a read-only bridge from Level 19 observation state to X-axis structural anchors. It derives entry, invalidation, and destination anchors from the latest visible event or Hook/ND fallback, computes RR-like readiness, and outputs readiness/block reasons without creating paper orders, broker requests, real orders, panel objects, renderer mutations, or chart-object changes.


## Level 21 — Paper Intent / No Order

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER.md
```

Level 21 adds `state_gate_level21_paper_intents.csv`, converting a ready Level 20 Entry Bridge row into a paper intent seed with direction, entry price, stop price, target price, RR-like value, geometry status, allowed/blocked status, and block reason. It remains CSV-only, print-silent by default, panel-off by default, and adds no paper order, broker request, volume sizing, real order, renderer mutation, or chart-object change.


## Level 22 — Paper Lifecycle Close-Only

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY.md
```

Level 22 adds `state_gate_level22_paper_lifecycle.csv`, reconstructing a close-only lifecycle for the Level 21 paper intent. It tracks blocked, pending, entered-by-close, target-by-close, stop-by-close, expired, open, and ambiguous states, plus close-only MFE/MAE and realized R-like metrics, without creating paper orders, broker requests, real orders, volume sizing, renderer mutations, or chart-object changes.


## Level 23 — Paper Performance Close-Only

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY.md
```

Level 23 adds `state_gate_level23_paper_performance.csv`, summarizing the close-only paper lifecycle from Level 22 into research performance metrics such as target count, stop count, expired count, open count, ambiguous count, hit-rate-like, loss-rate-like, average R-like, best R-like, and worst R-like. It remains CSV-only, print-silent by default, panel-off by default, and adds no paper orders, broker requests, real orders, volume sizing, risk sizing, renderer mutation, or chart-object change.


## Level 24 — Safety Gate / Pre-Broker Guard

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER.md
```

Level 24 adds `state_gate_level24_safety_gate.csv`, a pre-broker safety gate that evaluates license status, symbol allow-list, timeframe allow-list, spread, Level 23 paper performance thresholds, manual arm state, and the requirement that real execution remains disabled. It remains CSV-only, print-silent by default, panel-off by default, and adds no paper orders, broker requests, real orders, volume sizing, risk sizing, renderer mutation, or chart-object change.


## Level 25 — Broker Dry Run Only

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY.md
```

Level 25 adds `state_gate_level25_broker_dry_run.csv`, a broker-like request preview that depends on Level 24 Safety Gate and Level 21 Paper Intent. It emits dry-run-only request fields such as preview order type, entry price, SL, TP, magic, comment, and block reason, while keeping volume at zero and avoiding OrderSend, CTrade, OrderCheck, real execution, risk sizing, renderer mutation, or chart-object changes.


## Level 26 — Broker Request Validator / No Send

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_26_BROKER_VALIDATOR_NO_SEND.md
```

Level 26 adds `state_gate_level26_broker_validator.csv`, validating the Level 25 broker dry-run preview against no-send requirements, zero-volume lock, normalized prices, tick-size alignment, directional geometry, and broker stop-level distance. It remains CSV-only, print-silent by default, panel-off by default, and adds no OrderSend, OrderCheck, CTrade, broker request, real order, position, volume sizing, risk sizing, renderer mutation, or chart-object change.


## Level 27 — Broker Request Ledger / No Send

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_27_BROKER_REQUEST_LEDGER_NO_SEND.md
```

Level 27 adds `state_gate_level27_broker_request_ledger.csv` and `latest_state_gate_level27_broker_request_ledger.csv`, recording dry-run broker preview requests and Level 26 validator outcomes into an append-only no-send ledger with duplicate skipping. It remains CSV-only, print-silent by default, panel-off by default, and adds no OrderSend, OrderCheck, CTrade, broker request, real order, position, volume sizing, risk sizing, renderer mutation, or chart-object change.


## Level 28 — Broker Request Audit / No Send

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_28_BROKER_REQUEST_AUDIT_NO_SEND.md
```

Level 28 adds `state_gate_level28_broker_request_audit.csv` and `latest_state_gate_level28_broker_request_audit.csv`, auditing the no-send broker request chain for dry-run-only integrity, zero-volume integrity, no-send contract integrity, request-validator coherence, and safety/intent coherence. It remains CSV-only, print-silent by default, panel-off by default, and adds no OrderSend, OrderCheck, CTrade, broker request, real order, position, volume sizing, risk sizing, renderer mutation, or chart-object change.


## Level 29 — Paper Broker Adapter / Still No Send

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_29_PAPER_BROKER_ADAPTER_NO_SEND.md
```

Level 29 adds `state_gate_level29_paper_broker_adapter.csv` and `latest_state_gate_level29_paper_broker_adapter.csv`, registering a validated and audited no-send request chain as an internal paper-broker adapter record with a virtual ticket, paper order state, adapter status, and block reason. It remains CSV-only, print-silent by default, panel-off by default, and adds no OrderSend, OrderCheck, CTrade, broker request, real order, position, volume sizing, risk sizing, renderer mutation, or chart-object change.


## Level 30 — Paper Broker Lifecycle / Still No Send

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_30_PAPER_BROKER_LIFECYCLE_NO_SEND.md
```

Level 30 adds `state_gate_level30_paper_broker_lifecycle.csv` and `latest_state_gate_level30_paper_broker_lifecycle.csv`, tracking the internal virtual ticket created by Level 29 through a close-only paper-broker lifecycle with pending, active, target, stop, expired, ambiguous, and blocked states. It remains CSV-only, print-silent by default, panel-off by default, and adds no OrderSend, OrderCheck, CTrade, broker request, real order, position, volume sizing, risk sizing, renderer mutation, or chart-object change.


## Stabilization Patch 01 — Level 24-30 No-Send Chain

```text
docs/flag_counting/FLAG_COUNTING_STABILIZATION_PATCH_01_LEVEL_24_30.md
```

This patch does not add a new level. It stabilizes the Level 24-30 no-send chain by making Level 27-30 exporters respect the master `export_csv` switch, fixing latest/append row write-state flags before serialization, trimming Level 24 allow-list tokens correctly, and adding simple prefix wildcard support for allow-list values such as `GOLD*` or `PERIOD_M*`. It adds no OrderSend, OrderCheck, CTrade, broker request, real execution, volume sizing, risk sizing, renderer mutation, or chart-object mutation.


## Consolidation Patch 01 — No-Send Context

```text
docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_01_NO_SEND_CONTEXT.md
```

Consolidation Patch 01 adds a shared latest-state no-send context snapshot at `latest_consolidation_01_no_send_context.csv`. It caches the latest rows from Level 20, 21, 24, 25, 26, 27, 28, 29, and 30, then exports one consolidated context row. It does not add Level 31, does not change execution behavior, and adds no OrderSend, OrderCheck, CTrade, broker requests, real orders, positions, volume sizing, risk sizing, renderer mutation, or chart-object changes.


## Consolidation Patch 02 — Final No-Send Decision State

```text
docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_02_FINAL_DECISION_STATE.md
```

Consolidation Patch 02 adds `final_no_send_decision_state.csv`, a human-readable latest-state dashboard generated from the Consolidation Patch 01 no-send context. It summarizes setup state, chain stage, blocker layer, blocker reason, request id, virtual ticket, entry, SL, TP, paper lifecycle status, paper order state, realized R-like, and no-send integrity. It does not add Level 31, does not change execution behavior, and adds no OrderSend, OrderCheck, CTrade, broker requests, real orders, positions, volume sizing, risk sizing, renderer mutation, or chart-object changes.


## Consolidation Patch 03 — Duplicate Rebuild Reduction

```text
docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_03_DUPLICATE_REBUILD_REDUCTION.md
```

Consolidation Patch 03 reduces repeated internal rebuilds in Level 26 through Level 30 by reusing the latest-row caches introduced in Consolidation Patch 01. It keeps fallback rebuild paths when caches are unavailable, preserves all current outputs, updates context caches after rows are built, and adds no OrderSend, OrderCheck, CTrade, broker requests, real orders, positions, volume sizing, risk sizing, renderer mutation, or chart-object changes.


## Consolidation Patch 04 — Final CSV Field Normalization

```text
docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION.md
```

Consolidation Patch 04 adds `final_no_send_decision_state_normalized.csv`, a machine-friendly normalized final decision snapshot with schema version, integer boolean flags, direction sign, separated request fields, price fields, risk/reward fields, lifecycle fields, blocker fields, and no-send integrity. It does not add Level 31, does not change execution behavior, and adds no OrderSend, OrderCheck, CTrade, broker requests, real orders, positions, volume sizing, risk sizing, renderer mutation, or chart-object changes.


## Consolidation Patch 05 — Runtime Health Summary

```text
docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_05_RUNTIME_HEALTH_SUMMARY.md
```

Consolidation Patch 05 adds `runtime_no_send_health_summary.csv`, a latest-state health snapshot for the no-send stack. It summarizes context readiness, final decision readiness, normalized CSV quality, no-send integrity, expected output enablement, setup state, chain stage, blocker layer, request id, virtual ticket, prices, request volume, and realized R-like. It does not add Level 31, does not change execution behavior, and adds no OrderSend, OrderCheck, CTrade, broker requests, real orders, positions, volume sizing, risk sizing, renderer mutation, or chart-object changes.
