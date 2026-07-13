# NDS F2 Higher-Timeframe F3 Exit — Audit Report

## Scope

This patch adds a third exit mode to the dedicated F2 Waist-Break Point-2 Strategy Tester profile.

```text
FP_NDS_F2_EXIT_FIXED_F2_FLAG_END
FP_NDS_F2_EXIT_F3_FLAG_RETEST
FP_NDS_F2_EXIT_HIGHER_TIMEFRAME_F3_FLAG_RETEST
```

The new mode holds each lower-timeframe trade until a canonical same-direction F3 on a configurable higher timeframe forms Leg1 and then its own Waist. The Waist is the correction gate; TP is placed at the endpoint of that exact F3 Leg1.

Default higher-timeframe exit input:

```text
InpF2BTF3ExitHigherTimeframe = PERIOD_H1
```

## Canonical behavior

### Entry and risk

No entry geometry changed:

```text
Entry = final Point-2 limit behind F2 Waist
Stop  = behind direct parent F1 Waist
```

### Reward/Risk authority

No RR authority changed:

```text
RR Reference = original lower-timeframe F2 Leg2 endpoint
```

The future HTF F3 target is not used for admission or entry repricing because it does not exist at setup time.

### Higher-timeframe dynamic exit

```text
position fills
→ position-specific HTF search boundary is frozen
→ first eligible same-direction canonical HTF F3 Leg1 is locked
→ the same locked F3 forms its Waist
→ TP becomes that exact Leg1 endpoint
→ only the bound position ticket is modified or closed
```

## Per-trade isolation

Each dynamic context now stores:

- exit mode and exit timeframe;
- position open time;
- position-specific search boundary;
- HTF F3 sequence and parent-sequence identity;
- HTF F3 scale;
- exact Leg1 node ID, time and price;
- exact Waist node ID, time and price;
- dynamic target, correction and TP state.

Multiple trades may legitimately observe the same HTF F3, but no mutable exit state is shared between tickets.

## Candidate selection

The selected candidate must be:

- F3 level;
- same direction as the open position;
- canonical `visible_main`;
- structurally valid;
- equipped with Leg1;
- temporally after the position-specific HTF entry boundary.

The first eligible Leg1 is selected. Equal-time candidates are resolved by canonical priority and deterministic event ordering. Runtime identity does not depend on event ID alone; sequence, scale, Leg1 node ID and Leg1 time are locked.

## Correction and target

A generic pullback is not accepted. The correction must be the Waist of the same locked F3:

```text
same F3: pos_waist > pos_leg1
```

Only then is `dynamic_target_price` set to that F3 Leg1 price.

## Invalidation

The HTF scan retains invalidated candidates in its audit stream. A locked candidate that invalidates before producing a valid Waist is released, the position-specific search boundary advances, and the position waits for the next eligible HTF F3.

## Interaction with the HTF entry filter

Entry filtering and exit management are independent:

- the HTF F-phase gate controls new orders;
- the HTF F3 exit controls existing positions.

An existing position continues waiting for its HTF F3 exit even if the entry gate later closes or enters Hook/ND.

## Performance

The full canonical HTF scan runs only when:

1. the new HTF F3 exit mode is selected;
2. at least one managed position is open;
3. a new configured HTF bar has opened.

The event stream is cached between HTF bars. The entry-timeframe detector does not scan F3 in HTF exit mode.

No runtime print, CSV, renderer, timer, chart object or AI layer was added.

## Timeframe validation

The configured exit timeframe must be strictly higher than the entry chart timeframe. Invalid combinations fail initialization with `INIT_PARAMETERS_INCORRECT`.

## Versions

```text
Expert Version: 1.80
Contract: NDS-F2-WAIST-BREAK-09
Schema: nds_f2_waist_break_point2_v9
```

## Validation performed

Passed:

- dedicated HTF F3 exit contract QA;
- local exact per-trade F3 regression QA;
- dual-exit regression QA;
- HTF F-phase filter regression QA;
- overlap and RR repricing regression QA;
- hedge and parallel-context regression QA;
- F2 Waist-Break contract QA;
- lightweight backtest runtime QA;
- brace, parenthesis and bracket balance checks;
- no-print/no-file/no-render runtime checks;
- ZIP path and integrity checks.

MetaEditor is not available in this environment. Final MQL5 compilation and Strategy Tester execution must be performed locally.
