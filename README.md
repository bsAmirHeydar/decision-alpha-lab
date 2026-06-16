# Decision Alpha Lab

A research-first quantitative trading laboratory.

## Runtime Direction

The active runtime is now **MQL5-native**.

Python, FastAPI, React, Parquet cache pipelines, and external bridge/watch loops have been removed from the active execution path. The archived Python implementation should remain in the branch:

```text
archive/python-brain-m0001
```

Current active development should happen on:

```text
mql-native-migration
```

## Why MQL-native

The project needs fast, live-safe, visually auditable iteration inside MT5 Strategy Tester and charts. A separate Python process introduced asynchronous delay, shared-file friction, CSV adapter complexity, and live-semantics ambiguity.

MQL5 now owns:

- market data access
- L-rule structural node detection
- M0001 RTV event construction
- visual validation
- tester behavior
- validation journal export

## MQL5 Entry Points

Expert:

```text
mql5/Experts/DecisionAlphaLab/M0001/M0001_LiveVisualLab.mq5
```

Includes:

```text
mql5/Include/DecisionAlphaLab/
```

Validation export script:

```text
mql5/Scripts/DecisionAlphaLab/M0001/M0001_ExportValidationJournal.mq5
```

## Research Structure

The lab workflow remains:

```text
lab/01_observation
lab/02_hypotheses
lab/03_experiments
lab/04_analysis
lab/05_validation
lab/06_production
lab/07_monitoring
lab/08_archive
```

The runtime changed. The research discipline did not.

## Apply Locally

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\apply_mql_native_migration.ps1
```

To also copy files into an MT5 terminal data folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\apply_mql_native_migration.ps1 -TerminalDataPath "C:\Users\<YOU>\AppData\Roaming\MetaQuotes\Terminal\<TERMINAL_ID>"
```

Then compile:

```text
MQL5/Experts/DecisionAlphaLab/M0001/M0001_LiveVisualLab.mq5
```

## Documentation

- `docs/mql_native/MQL_NATIVE_ARCHITECTURE.md`
- `docs/mql_native/M0001_MQL_NATIVE_SPEC.md`
- `docs/mql_native/MODULE_MAP.md`


## M0001 node price labels

In the MQL-native runtime, `InpShowNodePrices` displays node prices as local text
labels above high-node markers and below low-node markers. Full horizontal
node-price lines are disabled by default and controlled separately by
`InpShowNodePriceLines`.


## Live bar stream

The MQL-native runtime processes bars as a live stream by default. It does not
bulk-copy the whole test window for active logic. On each new closed candle, it
reads only the newly closed bar, appends it to an in-memory rolling stream, and
updates L-rule nodes, M0001 events, and visual audit objects.


## Clean arrow node markers

M0001 MQL-native now uses clean arrow markers by default:

```text
InpNodeMarkerStyle = 0
```

This removes diagonal chevron wing lines around candles. When
`InpShowNodePrices=true`, node prices are shown as local text labels above
high-node arrows and below low-node arrows.


## Node price lines hard-disabled

M0001 no longer draws full-chart horizontal node price lines.  
`InpShowNodePriceLines` is retained only for backward compatibility and is ignored.

Use:

```text
InpShowNodePrices = true
```

to show local price text above high-node arrows and below low-node arrows.


## Strict node markers

M0001 node visualization is now arrow-only by default.  
The visual layer no longer draws chevron wing trend segments or full-chart node
price lines. Node prices are shown as local text labels when
`InpShowNodePrices=true`.


## Arrow anchor compile fix

M0001 strict node markers use `OBJ_ARROW`. The arrow anchor helper now passes
anchor values as integers to avoid MetaEditor enum ambiguity between arrow and
text anchor constants.


## M0001 hard clean visual

The MQL-native visual layer can purge chart trace lines and main-window indicators
so node inspection is arrow + local price text only.

```text
InpPurgeTraceLines = true
InpPurgeMainWindowIndicators = true
InpHighNodePriceTextGapPoints = 120
InpLowNodePriceTextGapPoints = 120
```


## M0001 extreme and live hunt zone audit

After structural nodes are validated, M0001 now exposes an audit layer for:

```text
node -> expansion extreme -> live hunt/territory zone
```

Inputs:

```text
InpShowExpansionExtremes = true
InpShowLiveHuntZones = true
InpShowInvalidatedHuntZones = false
```

The L-rule structural node detector is available through the stable facade:

```text
mql5/Include/DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh
```


## Hunt zone origin from node

M0001 live hunt/territory rectangles now start from the original node candle
instead of the active-from candle. The logic still confirms nodes at
`node_index + L`; this change only makes the visual rectangle's structural origin
match the node itself.


## Consumed node repair

M0001 now treats consumed/hunted nodes as finished.  
After consumption, the node no longer draws an active expansion-extreme line or
live hunt zone. A small consumed marker can be shown with:

```text
InpShowConsumedNodeMarkers = true
```


## Consumed zone history

Consumed M0001 hunt zones now remain visible as historical rectangles from the
node origin to the consume candle.

```text
InpShowConsumedHuntZoneHistory = true
```

They do not extend beyond the consume candle.


## Consumed extreme history

Consumed M0001 nodes now keep their final node-to-extreme audit line on the chart,
but the line stops updating after the consume candle.

```text
InpShowConsumedExtremeHistory = true
```

The underlying audit state freezes `expansion_extreme` when the node is consumed.


## Unbounded backtest data

M0001 no longer limits Strategy Tester runs to an arbitrary candle count.

```text
InpBars = 0
```

means use all available bars in the tester's selected date range/history. Positive
values still act as an optional cap for performance.


## Latest visual caps

Visual caps now show latest N objects instead of oldest N objects.

```text
InpMaxNodesToDraw = 2
```

draws the latest 2 nodes. `InpBars` remains a data cap, so keep `InpBars=0` for
full Strategy Tester history.


## Node visibility diagnostics

The M0001 summary can now show computed node count, visual draw caps, audit-state
count, and latest computed node information.

```text
InpShowNodeVisibilityDebug = true
```

This separates data limits from visual limits and from normal L-rule confirmation
behavior.


## Viewport visual renderer

M0001 now renders chart objects only for the current visible chart window by
default. This keeps the full engine unbounded while avoiding MT5 chart-object
overload.

```text
InpDrawOnlyVisibleWindow = true
InpVisibleWindowPaddingBars = 80
InpRedrawOnChartChange = true
```


## Two-mode node consumption

M0001 supports explicit node consumption modes:

```text
InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT
InpConsumeMode = DAL_M0001_CONSUME_BY_TOUCH
```

HUNT consumes only on node-price break. TOUCH consumes on first territory-zone
touch. The selected mode is applied in audit-state computation and event state,
not only in visualization.


## Touch consumes after event completion

M0001 touch mode follows the original README semantics:

```text
first zone touch -> event starts
event closes after exit_gap outside frozen event territory -> node consumed
```

Touch no longer consumes immediately on the first touch candle. Hunt mode remains
node-break based and can support revisits until the node is hunted.


## Pending touch and hunt priority

A first zone touch starts a pending touch event. TOUCH is confirmed only after
`InpExitGap` consecutive candles outside the frozen event zone. If the node price
is broken before that confirmation, the pending touch converts to `CONSUMED:HUNT`.
