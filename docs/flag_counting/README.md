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



## Level 19 state gate and dashboard

Phoenix Level 19 is specified as a read-only multi-timeframe State Gate. It does not change Node, Hook/ND, Flag Body, Internal Count, F1/F2/F3, ownership, canonicalization, renderer, validation, release, or license logic. It projects the locked anatomy into a live M1/M10/H1 state map and a top-right minimizable dashboard.

Read:

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md
docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md
docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md
docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION.md
docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md
docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE5_PANEL_POLISH.md
docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE.md
```

Phase 2 implements the closed-bar tracker for the three configured State Gate timeframes. Phase 3 projects Rally View from the existing locked F1/F2/F3 event lifecycle output. Phase 4 projects Hook View from the existing locked Hook/ND branch output across the configured L-scale sequence. Phase 5 polishes the right-upper dashboard, adds configurable Rally/Hook preview limits, improves live debug readability, and exports `latest_state_gate_panel.csv`. Phase 6 stores a per-timeframe State Contract with stable `state_key`, anatomy status, storage status, and decision-neutral entry-bridge readiness labels for future entry-layer consumption.

## Level 18 static QA

Phoenix now has a final compile/static QA hardening pass. Runtime emits `FP_LEVEL18`; source-side scanning is available with:

```powershell
python tools/flag_counting/static_qa.py --root . --csv reports/flag_counting_static_qa.csv
```


## Level 19 — Phase 7

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES.md
```

Phase 7 moves the State Gate dashboard default anchor to the **left-upper** chart corner and adds independent minimize / restore controls for each timeframe block plus the Rally and Hook subsections.


## Level 19 — Phase 8

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE8_PANEL_VISIBILITY_FIX.md
```

Phase 8 adds a hard left-upper panel override and stronger panel contrast so old saved right-corner inputs cannot hide the dashboard body.


## Level 19 — Phase 9

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE9_VISUAL_DEBUG_CONTRACT.md
```

Phase 9 adds a visual/debug contract for the State Gate dashboard, including an on-panel diagnostics line, effective-corner export, and `latest_state_gate_diagnostics.csv`.


## Level 19 — Phase 9A

```text
docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE9A_COMPILE_FIX.md
```

Phase 9A fixes the missing `InpStateGateExportDiagnosticsCsv` input declaration used by the Phase 9 visual debug contract.
