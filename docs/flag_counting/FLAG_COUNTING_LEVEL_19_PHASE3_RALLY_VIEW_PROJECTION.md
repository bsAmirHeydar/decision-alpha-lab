# Flag Counting Level 19 — Phase 3 Rally View Projection

Status: implemented design note  
Parent spec: `FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md`  
Parent implementation plan: `FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md`

---

## 1. Purpose

Phase 3 upgrades Level 19 State Gate from a closed-bar tracker into the first real anatomy projection layer.

Phase 2 answered:

```text
Which configured timeframe has a new closed candle?
```

Phase 3 now also answers:

```text
For each configured timeframe, what is the current Rally View from the existing F-counting anatomy?
```

This is still not an entry engine.

It does not answer:

```text
Buy?
Sell?
Where is the order?
```

It only maps the locked Phoenix F1/F2/F3 output into a live multi-timeframe State Gate snapshot.

---

## 2. Non-negotiable boundary

Phase 3 does not change any locked anatomy logic.

It does not edit or override:

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

The new code only reads already-built Phoenix event fields.

The direction is strictly:

```text
locked Phoenix F-counting anatomy
        ↓
Level 19 Rally View rows
        ↓
panel / CSV / audit
```

No reverse dependency is allowed.

---

## 3. What Phase 3 adds

Phase 3 adds Rally View projection for the three configured State Gate timeframes.

Default timeframes remain:

```text
M1
M10
H1
```

They remain configurable through the existing Level 19 inputs.

For each timeframe, Phase 3 builds a closed-bar-only local anatomy read:

```text
Copy closed bars for the configured timeframe
Run the locked Phoenix detection pipeline on that timeframe
Read the resulting F1/F2/F3 event stream
Project the event stream into Rally rows
```

This means M1, M10, and H1 are not faked from the chart timeframe. Each configured timeframe gets its own closed-bar candle stream.

---

## 4. Rally View definition

Rally View is not a new Rally engine.

In this project:

```text
Rally View = the view produced by existing F-counting anatomy.
```

So Phase 3 does not introduce a separate `Rally` classifier.

It simply reads:

```text
F1 / F2 / F3 level
lifecycle status
body status
internal count
body points
sequence id
parent id
scale L
direction
canonical / visual / structural ids
```

and labels the current state.

---

## 5. Row selection

For each timeframe, the State Gate creates Rally rows from visible Phoenix F events only.

The display is capped by:

```text
InpStateGateMaxRallyRowsPerTf
```

Phase 3 prioritizes:

```text
1. latest established F
2. latest probable next F
3. additional recent visible F rows until the cap is reached
```

Only these F levels are displayed:

```text
F1
F2
F3
```

No F4+ label is emitted in Phase 3.

---

## 6. Latest established F

The latest established F is derived from existing lifecycle status only.

The projection treats the following as established:

```text
F1: confirmed / extended
F2: confirmed / extended
F3: completed / locked
```

The label format is compact:

```text
F2_ESTABLISHED|bull|confirmed
F3_ESTABLISHED|bear|locked
```

If no established F is available:

```text
NO_ESTABLISHED_F
```

---

## 7. Probable next F

The probable next F is also derived from existing Phoenix event fields only.

It uses non-established visible F rows such as candidate, post-flag, live-body, and body-complete states.

The label format is compact:

```text
F2_PROBABLE|bull|post_flag|POST_FLAG_BODY|AFTER_1_BEFORE_2
F1_PROBABLE|bear|candidate|IN_FLAG_BODY|PROBABLE_LEG2_BEFORE_LEG1_BREAK
```

If no probable next F is available:

```text
NO_PROBABLE_NEXT_F
```

---

## 8. Body state labels

Phase 3 maps body state into the dashboard vocabulary:

```text
IN_FLAG_BODY
POST_FLAG_BODY
F_ESTABLISHED
UNKNOWN_BODY_STATE
```

These labels are projections only. They do not decide lifecycle state.

---

## 9. In-flag stage labels

When a probable F is still inside its flag body, the projection may emit:

```text
PROBABLE_LEG1
LEG1_CORRECTION
PROBABLE_LEG2_BEFORE_LEG1_BREAK
PROBABLE_LEG2_AFTER_LEG1_BREAK
UNKNOWN_FLAG_STAGE
```

The Leg2 break label is derived from existing Leg1/Leg2 points:

```text
bullish: Leg2 price > Leg1 price
bearish: Leg2 price < Leg1 price
```

This is only a label. It is not a new F rule.

---

## 10. Post-flag stage labels

When a probable F is after its flag body, Phase 3 reads the existing internal count and maps it into:

```text
BEFORE_1
AFTER_1_BEFORE_2
AFTER_2_BEFORE_3
AFTER_3_BEFORE_4
AFTER_4_PLUS
```

When the event is already established:

```text
F_CONFIRMED_BY_FLAG_BREAK
```

This matches the user-level concept that F establishment means the flag has been crossed by the existing F-counting lifecycle.

---

## 11. CSV output

`latest_state_gate_rally.csv` now contains projected Rally rows instead of Phase 2 placeholders.

Key columns include:

```text
symbol
slot
timeframe
closed_bar_time
source_event_id
sequence_id
parent_event_id
scale_L
direction
f_level
latest_established_f
probable_next_f
body_state
flag_stage
post_flag_stage
source_id
label
```

Hook CSV remains a Phase 4 placeholder.

---

## 12. Panel output

The chart panel summary line now shows per timeframe:

```text
latest established F summary
probable next F summary
```

The panel remains compact and right-top minimizable.

It still does not display entry permission, order side, or trade instruction.

---

## 13. Timer behavior

`OnTimer()` now runs the same Level 19 Phase 3 State Gate path with quiet internal anatomy settings.

This allows the configured M1/M10/H1 closed-bar State Gate to update even if the chart timeframe itself has not produced a new bar.

The timer path suppresses internal Node/Hook/F print spam and prints only compact Level 19 audit when a configured timeframe changes or errors occur.

---

## 14. Failure labels

If a timeframe has no usable data or no visible F rows, Phase 3 emits safe debug labels:

```text
TF_DATA_UNAVAILABLE
NO_CANONICAL_F_ROWS
NO_ESTABLISHED_F
NO_PROBABLE_NEXT_F
```

These are not trading signals and not engine failures by themselves.

They only show what the State Gate could or could not project.

---

## 15. What remains for Phase 4

Phase 4 must implement Hook View projection.

It should read existing Hook/ND and node-count output across L scales and map them into:

```text
hook polarity
latest confirmed node
current node number
latest high node
latest low node
sequence / hook id
scale L
```

Phase 4 must keep the same invariant:

```text
read-only projection only; no Hook/ND logic changes.
```

---

## 16. Done definition for Phase 3

Phase 3 is done when:

```text
1. State Gate still updates only from closed candles.
2. M1/M10/H1 each run their own timeframe-specific anatomy read.
3. Rally View rows are projected from existing F1/F2/F3 event fields.
4. Latest established F is shown per timeframe when available.
5. Probable next F stage is shown per timeframe when available.
6. CSV rally rows are written with source event and sequence ids.
7. Panel summary shows established/probable Rally state.
8. Hook rows remain explicitly pending for Phase 4.
9. Existing Node, Hook/ND, F-counting, ownership, canonicalization, renderer, validation, release, and license logic remain untouched.
```
