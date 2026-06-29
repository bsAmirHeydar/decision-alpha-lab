# Flag Counting Level 19 — Phase 2 Closed-Bar Tracker

Status: implemented scope note
Parent documents:

```text
FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md
FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md
```

---

## Purpose

Phase 2 turns the Level 19 State Gate from a visual/input shell into a live closed-bar state store.

It tracks the latest closed candle independently for each configured State Gate timeframe:

```text
InpStateGateTf1 = PERIOD_M1
InpStateGateTf2 = PERIOD_M10
InpStateGateTf3 = PERIOD_H1
```

The tracker is deliberately read-only. It does not project Rally View yet and does not project Hook View yet. Those remain Phase 3 and Phase 4.

---

## Locked logic boundary

Phase 2 does not change any locked anatomy logic:

```text
Node logic
Hook / ND logic
Flag Body logic
Internal Count logic
F1 lifecycle logic
F2 lifecycle logic
F3 lifecycle logic
Ownership logic
Canonicalization logic
Renderer logic
Validation logic
Release logic
License logic
```

Phase 2 only adds state storage around closed-bar timing and panel/export refresh decisions.

---

## New behavior

For each configured timeframe slot, Level 19 now stores:

```text
timeframe
last closed bar time
previous closed bar time
last closed bar close
whether closed-bar data is available
whether the slot is dirty
available bar count
slot update count
tracker status
reason
```

A timeframe is marked dirty when:

```text
1. the slot sees its first valid closed candle, or
2. the latest closed-bar time changes from the previously processed closed-bar time.
```

If the closed-bar time is unchanged, the slot is marked:

```text
CLOSED_BAR_UNCHANGED
```

If shift-1 data is unavailable, the slot is marked:

```text
TF_DATA_UNAVAILABLE
```

---

## Update cadence

The tracker uses closed candles only:

```text
latest_closed_bar_time  = iTime(_Symbol, tf, 1)
latest_closed_bar_close = iClose(_Symbol, tf, 1)
```

Shift `1` is mandatory. The still-forming candle is not used as the canonical State Gate state.

---

## Timer behavior

Phase 2 also connects Level 19 to `OnTimer()`.

This allows the State Gate to keep checking the selected timeframes without waiting for the chart timeframe itself to close.

The timer call is lightweight at Phase 2 because it only updates closed-bar tracking and dashboard/export state. It does not run or mutate the locked Phoenix anatomy engines.

---

## Panel behavior

The top-right State Gate panel now displays the closed-bar tracker state for each configured timeframe.

The panel redraws when:

```text
1. a configured timeframe becomes dirty, or
2. the panel has not been drawn yet.
```

Minimize/restore behavior remains owned by `FP_StateGatePanel`.

---

## CSV behavior

Phase 2 writes live latest-state CSV artifacts when export is enabled:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_summary.csv
MQL5/Files/FlagCountingPhoenix/latest_state_gate_rally.csv
MQL5/Files/FlagCountingPhoenix/latest_state_gate_hooks.csv
MQL5/Files/FlagCountingPhoenix/latest_state_gate_manifest.csv
```

The Rally and Hook CSV files still contain projection-pending placeholder rows. This is intentional until Phase 3 and Phase 4.

---

## New inputs

Phase 2 adds explicit export controls:

```text
InpStateGateExportOverwriteLatest = true
InpStateGateExportFolder = "FlagCountingPhoenix"
```

These keep Level 19 export behavior aligned with Phoenix latest-file export style.

---

## Audit lines

Runtime emits:

```text
FP_LEVEL19_STATE_GATE
FP_LEVEL19_STATE_GATE_SAMPLE
```

Timer-only dirty updates may emit:

```text
FP_LEVEL19_STATE_GATE_TIMER
```

No buy/sell, entry, or trade-permission labels are produced.

---

## Done definition for Phase 2

Phase 2 is considered implemented when:

```text
1. each configured timeframe has independent closed-bar time tracking;
2. dirty flags are true only on first snapshot or new closed bars;
3. the State Gate can update from OnTimer without touching F/Hook/ND logic;
4. panel redraw is controlled by dirty state;
5. latest CSV files are written for tracker/debug state;
6. Rally/Hook projection rows remain explicit placeholders;
7. static QA reports no blocking failures.
```
