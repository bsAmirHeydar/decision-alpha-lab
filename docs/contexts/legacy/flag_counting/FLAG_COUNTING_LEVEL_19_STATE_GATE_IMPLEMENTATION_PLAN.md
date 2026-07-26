# Flag Counting Level 19 — State Gate and Dashboard Implementation Plan

Status: implementation plan
Parent spec: `FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md`
Target: read-only multi-timeframe state map above locked Phoenix anatomy

---

## 1. Implementation principle

Level 19 must be implemented as a read-only layer after the existing Phoenix anatomy pipeline.

It must not change:

```text
Node logic
Hook/ND logic
Flag body logic
Internal count logic
F1/F2/F3 lifecycle logic
Ownership logic
Canonicalization logic
Renderer logic
Validation logic
License logic
```

The implementation must behave like a projection:

```text
locked Phoenix anatomy -> Level 19 State Gate snapshot -> panel/export/audit
```

The State Gate is not a strategy engine.

---

## 2. Proposed module set

Add new include modules under:

```text
mql5/Include/FlagCountingPhoenix/
```

Recommended files:

```text
FP_StateGateTypes.mqh
FP_StateGateRules.mqh
FP_StateGateEngine.mqh
FP_StateGatePanel.mqh
FP_StateGateExport.mqh
FP_StateGateAudit.mqh
```

Responsibilities:

### FP_StateGateTypes.mqh

Owns enums and structs:

```text
FP_StateGateConfig
FP_StateGateSnapshot
FP_StateGateTimeframeState
FP_StateGateRallyRow
FP_StateGateHookRow
FP_StateGatePanelState
```

### FP_StateGateRules.mqh

Pure label/projection rules:

```text
Map F lifecycle to latest established F label
Map probable next F to body/post-flag stage
Map Hook/ND context to hook polarity and node label
Map timeframe to display name
Cap rows for dashboard view
```

No mutation is allowed in this file.

### FP_StateGateEngine.mqh

Owns runtime update orchestration:

```text
track closed-bar time per timeframe
run/read Phoenix anatomy state per configured timeframe
build snapshot
store last snapshot
trigger panel/export/audit
```

### FP_StateGatePanel.mqh

Owns chart objects:

```text
background rectangle
title bar
minimize button
text rows
timeframe sections
object naming and cleanup
```

### FP_StateGateExport.mqh

Writes:

```text
latest_state_gate_summary.csv
latest_state_gate_rally.csv
latest_state_gate_hooks.csv
latest_state_gate_manifest.csv
```

### FP_StateGateAudit.mqh

Prints compact audit lines:

```text
FP_LEVEL19_STATE_GATE
FP_LEVEL19_RALLY
FP_LEVEL19_HOOK
```

---

## 3. Expert input integration

Add inputs to `FlagCountingPhoenixExperiment.mq5` in a new input group:

```text
input group "Level 19 - State Gate Dashboard"
input bool            InpStateGateEnabled              = true;
input ENUM_TIMEFRAMES InpStateGateTf1                  = PERIOD_M1;
input ENUM_TIMEFRAMES InpStateGateTf2                  = PERIOD_M10;
input ENUM_TIMEFRAMES InpStateGateTf3                  = PERIOD_H1;
input bool            InpStateGatePanelEnabled         = true;
input bool            InpStateGatePanelStartMinimized  = false;
input int             InpStateGatePanelX               = 16;
input int             InpStateGatePanelY               = 24;
input int             InpStateGatePanelWidth           = 520;
input int             InpStateGatePanelFontSize        = 8;
input int             InpStateGateMaxRallyRowsPerTf    = 6;
input int             InpStateGateMaxHookRowsPerTf     = 10;
input bool            InpStateGateShowIds              = true;
input bool            InpStateGateShowScaleL           = true;
input bool            InpStateGateExportCsv            = true;
input bool            InpStateGatePrintAudit           = true;
```

The final naming may be adjusted to match existing Phoenix conventions, but the semantics must remain.

---

## 4. Integration point in Phoenix

Level 19 should run after the existing canonical state is available.

Recommended order:

```text
Level 01-11   anatomy and canonicalization
Level 11.5    raw audit export
Level 12      renderer
Level 13-18   validation/release/interface/acceptance/static QA
Level 19      State Gate snapshot + panel + export
```

If Level 19 needs canonical rows before renderer, it may build its snapshot after canonicalization and draw its panel after the main renderer. The key invariant is that Level 19 must not affect any prior level.

---

## 5. Multi-timeframe architecture

Level 19 must maintain three independent timeframe states.

For each configured timeframe:

```text
state_tf[i].timeframe
state_tf[i].last_processed_closed_bar_time
state_tf[i].latest_snapshot
```

On each timer/tick pulse:

```text
1. For each configured timeframe, get latest closed bar time.
2. If closed bar time changed, mark that timeframe dirty.
3. Rebuild State Gate state for dirty timeframe.
4. Refresh panel if any timeframe changed.
5. Export CSV if enabled and any timeframe changed.
```

The implementation must avoid recomputing heavy anatomy unnecessarily.

---

## 6. Closed-bar detection

For each timeframe:

```text
latest_closed_bar_time = iTime(_Symbol, tf, 1)
latest_closed_bar_close = iClose(_Symbol, tf, 1)
```

Shift `1` is used for closed-bar state.

The system must not use the still-forming candle as the canonical Level 19 state.

---

## 7. Timeframe-specific anatomy source

The implementation must obtain Phoenix anatomy for each configured timeframe without changing the locked logic.

Preferred approach:

```text
Instantiate or reuse isolated per-timeframe Phoenix state containers.
Each timeframe must run the same locked Node/Hook/F pipeline on its own candle stream.
Level 19 then projects the resulting canonical rows into State Gate rows.
```

Forbidden shortcut:

```text
Do not project M1 anatomy as if it represented M10 or H1.
```

Each configured timeframe must have its own anatomy state.

---

## 8. Rally projection implementation

For each timeframe, read existing F lifecycle / canonical events and build Rally rows.

Step logic:

```text
1. Collect relevant canonical F events/sequences.
2. Restrict F-level display to F1/F2/F3.
3. Find latest established F level from locked lifecycle status.
4. Identify probable next F level from current sequence state.
5. Map body state to IN_FLAG_BODY or POST_FLAG_BODY.
6. If IN_FLAG_BODY, map body stage to:
   - PROBABLE_LEG1
   - LEG1_CORRECTION
   - PROBABLE_LEG2_BEFORE_LEG1_BREAK
   - PROBABLE_LEG2_AFTER_LEG1_BREAK
7. If POST_FLAG_BODY, map internal count to:
   - BEFORE_1
   - AFTER_1_BEFORE_2
   - AFTER_2_BEFORE_3
   - AFTER_3_BEFORE_4
   - AFTER_4_PLUS
8. Store source IDs for audit.
```

No new F-counting rule is allowed.

If a stage cannot be derived from existing Phoenix fields, set:

```text
UNKNOWN_FLAG_STAGE
UNKNOWN_POST_FLAG_STAGE
```

and document the missing source field.

---

## 9. Hook projection implementation

For each timeframe, read existing Hook/ND contexts and node states.

Step logic:

```text
1. Collect relevant Hook/ND contexts across the configured L list.
2. Sort from larger L to smaller L unless user changes display order later.
3. For each hook, derive polarity:
   - HOOK+ / ND+
   - HOOK- / ND-
4. Read latest confirmed high node and low node where available.
5. Read latest/current node number where available.
6. Map price position to a Hook position label.
7. Store hook id, sequence id, L, polarity, node number, high/low node ids/prices.
```

No new Hook/ND rule is allowed.

If a hook's current-node position cannot be fully resolved, use the simplest available label:

```text
CURRENT_NODE_N1
CURRENT_NODE_N2
CURRENT_NODE_N3
CURRENT_NODE_N4_PLUS
UNKNOWN_HOOK_POSITION
```

---

## 10. Dashboard panel implementation

Use MT5 chart objects with a strict object prefix, for example:

```text
FP_L19_STATE_GATE_
```

Required object types may include:

```text
OBJ_RECTANGLE_LABEL for background/title blocks
OBJ_LABEL for text rows
OBJ_BUTTON or label-click target for minimize/restore
```

The panel must support:

```text
top-right placement
minimized state
expanded state
row redraw without leaking objects
cleanup on deinit
```

Object lifecycle rules:

```text
1. Create/recreate panel only through FP_StateGatePanel.
2. Never reuse main renderer object names.
3. On each redraw, delete or update only Level 19 objects.
4. On deinit, remove all objects with FP_L19_STATE_GATE_ prefix.
```

---

## 11. Minimize behavior

Panel starts in:

```text
InpStateGatePanelStartMinimized
```

When minimized:

```text
show one compact title/header row only
hide all timeframe rows
keep state engine active
keep CSV export active if enabled
```

Minimization must never disable the State Gate state store.

---

## 12. CSV export implementation

Implement append-or-overwrite behavior consistent with existing Phoenix latest export style.

Recommended default:

```text
overwrite latest_state_gate_*.csv on each snapshot
```

This keeps the files as live latest-state artifacts, matching other Phoenix exports.

Files:

```text
latest_state_gate_summary.csv
latest_state_gate_rally.csv
latest_state_gate_hooks.csv
latest_state_gate_manifest.csv
```

The manifest should include:

```text
symbol
timeframe inputs
closed-bar mode
row counts
EA build
state gate version
export time
```

---

## 13. Audit implementation

Audit lines should be optional and compact.

Input:

```text
InpStateGatePrintAudit
```

Minimum lines:

```text
FP_LEVEL19_STATE_GATE
FP_LEVEL19_RALLY
FP_LEVEL19_HOOK
```

Long row details should prefer CSV over Print.

---

## 14. Validation and smoke tests

Level 19 needs a validation checklist but not a full trading test.

Required smoke tests:

```text
1. Attach EA to one symbol.
2. Enable State Gate.
3. Confirm panel appears top-right.
4. Confirm panel can minimize/restore.
5. Confirm M1 row updates only after M1 candle close.
6. Confirm M10 row updates only after M10 candle close.
7. Confirm H1 row updates only after H1 candle close.
8. Confirm Rally rows match visible Phoenix F labels for the same timeframe.
9. Confirm Hook rows match visible Phoenix Hook/ND labels for the same timeframe.
10. Confirm CSV files are created.
11. Confirm main Phoenix rendering is unchanged with Level 19 enabled/disabled.
12. Confirm static QA passes.
13. Confirm MetaEditor compile passes.
```

---

## 15. Development phases

### Phase 0 — Documentation freeze

Deliver:

```text
FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md
FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md
```

No code changes yet.

### Phase 1 — Input shell and module skeleton

Add:

```text
FP_StateGateTypes.mqh
FP_StateGateRules.mqh
FP_StateGateEngine.mqh
FP_StateGatePanel.mqh
FP_StateGateExport.mqh
FP_StateGateAudit.mqh
```

Add Level 19 inputs.

The first code patch should compile but may output placeholder rows.

### Phase 2 — Closed-bar timeframe tracker

Implement:

```text
per-timeframe closed-bar detection
last processed bar time
state dirty flags
```

No F/Hook projection yet.

### Phase 3 — Rally View projection

Implement latest established F and probable next F stage projection.

Must display up to F3 only.

Deliver:

```text
Rally rows in snapshot
Rally rows in CSV
Rally rows in panel
```

### Phase 4 — Hook View projection

Implement relevant Hook/ND list across L scales.

Deliver:

```text
Hook rows in snapshot
Hook rows in CSV
Hook rows in panel
```

### Phase 5 — Full panel polish

Implement:

```text
minimal top-right design
minimize/restore
row limits
ID visibility toggle
scale-L visibility toggle
object cleanup
```

### Phase 6 — Export and audit hardening

Implement final CSV columns and compact logs.

### Phase 7 — Validation and compile hardening

Run:

```powershell
python tools/flag_counting/static_qa.py --root . --csv reports/flag_counting_static_qa.csv
```

Then compile in MetaEditor and capture compile evidence.

### Phase 8 — Documentation update

Update:

```text
docs/contexts/legacy/flag_counting/README.md
FLAG_COUNTING_CURRENT_CANON.md or a Level 19 note pointing to the spec
VALIDATION_CASE_REGISTRY.md if new state-gate visual cases are added
```

---

## 16. Performance risks

Risk: Three independent timeframes may be heavy if the full Phoenix pipeline is recomputed frequently.

Mitigation:

```text
closed-bar only update
dirty timeframe tracking
row caps for panel
CSV overwrite only when changed
avoid tick-by-tick redraws
```

Risk: Hook rows may become very long across L scales.

Mitigation:

```text
panel row cap
full CSV export
large-to-small scale sorting
compact labels
```

Risk: M10 availability may differ by broker/history.

Mitigation:

```text
detect missing timeframe data
show TF_DATA_UNAVAILABLE
write manifest warning
keep other timeframes alive
```

---

## 17. Failure labels

Level 19 must display explicit safe labels when data cannot be derived:

```text
TF_DATA_UNAVAILABLE
NO_CANONICAL_F_ROWS
NO_RELEVANT_HOOK_ROWS
UNKNOWN_FLAG_STAGE
UNKNOWN_POST_FLAG_STAGE
UNKNOWN_HOOK_POSITION
STATE_GATE_DISABLED
```

These are not errors by themselves. They are debug labels.

---

## 18. Done definition

Level 19 is done when:

```text
1. It compiles.
2. It does not change existing Phoenix anatomy output.
3. It updates only on closed bars per timeframe.
4. It shows M1/M10/H1 by default.
5. It stores state even when minimized.
6. It renders a clean right-top minimizable panel.
7. It exports live state CSV files.
8. It shows latest established F and probable next F stage up to F3.
9. It shows relevant Hook/ND rows across L scales with polarity and current node status.
10. It can be used for visual debugging and future anatomy-to-entry design without producing entry signals.
```

---

## 19. Implementation summary

The implementation should be treated as Phoenix Level 19:

```text
Level 19 = State Gate + Dashboard
```

It is the first formal bridge from anatomy to entry thinking, but it remains decision-neutral.

It answers:

```text
What is the live state map of this symbol across M1/M10/H1?
Where are we in Rally View?
Where are we in Hook View?
Which IDs/sequences/scales are responsible for that state?
```

It deliberately does not answer:

```text
Should we enter?
Which side?
Where is the order?
```

That separation keeps the locked anatomy clean and prepares the next layer safely.
