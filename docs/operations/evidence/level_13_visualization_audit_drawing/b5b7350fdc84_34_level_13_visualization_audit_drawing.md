# Level 13 — Visualization / Audit Drawing

## Purpose

Level 13 adds chart-side audit drawings for EXEC001 STC SMT Cycles. It is still a no-order level. It does not change signal detection, paper execution, partial logic, hard-close logic, persistence, position management, or risk logic.

The drawing layer is designed to make the already-built execution stack inspectable on the chart:

- STC trading day zones.
- M1, M2, and M3 blocks.
- W1 through W4 boundaries.
- the active check candle.
- closed W high/low levels for the chart symbol.
- recent SMT paper-entry plans on the clean/traded symbol.
- SL, TP, and entry guide lines.
- W4 partial markers.
- 15:30 New York hard-close marker.
- same-check buy/sell ambiguity markers.
- dashboard label with current NY time, STC day id, M/W, and check index.

## Strict Non-Decision Rule

Drawing is audit-only. The renderer must never make a trading decision and must never modify the real strategy state.

The renderer can rebuild recent audit objects from current-day candles, but the output must be treated as a visualization of the existing decision rules, not a new strategy layer.

Level 13 still sends no real orders.

## Inputs

New Level 13 inputs:

- `InpWriteDrawingAudit`: write a CSV audit row on every drawing refresh.
- `InpDrawingRefreshSeconds`: minimum seconds between redraws.
- `InpDrawingHistoryChecks`: how many recent check candles to inspect for SMT/paper drawing.
- `InpDrawingHistoryWLevels`: how many closed W levels to draw.
- `InpDrawingClearOnDeinit`: remove STC drawing objects when the EA is removed.
- `InpDrawingObjectPrefix`: prefix for all chart objects.

Existing `InpEnableDrawing` remains the master drawing switch.

## Symbol behavior

The EA remains chart-symbol independent for decisions. However, price-specific drawings only make sense on a chart whose symbol is either `Symbol1` or `Symbol2`.

If the EA is attached to any other chart symbol:

- the dashboard is still drawn;
- M/W time zones are still drawn;
- price-specific W levels and SMT entry lines are suppressed;
- the drawing audit CSV records that the chart symbol was unsupported for price layers.

This avoids drawing SPX/NDX levels on an unrelated chart scale.

## Objects drawn

### 1. STC day/M/W time objects

The renderer draws the current STC day from 20:00 New York to 15:30 New York. It shows:

- M1: 20:00–02:00 NY.
- M2: 03:00–09:00 NY.
- M3: 09:30–15:30 NY.
- W boundaries inside each M.
- 15:30 NY hard-close line.

The time conversion uses the Level 02 time engine, including New York DST handling.

### 2. Active check candle

The current check-candle window is drawn and labeled with:

- check index;
- M cycle;
- W cycle.

This is visual audit only. The final-check no-entry rule remains controlled by the signal registry and paper-entry layers.

### 3. W levels

For the chart symbol, the renderer draws closed W high and low segments for the configured recent W history.

Each symbol still uses its own W levels. The renderer does not share price levels between symbols.

### 4. SMT / paper entry plans

For recent check candles, the renderer rebuilds the same structural SMT checks:

- W2 compares only with W1.
- W3 compares with W2 and W1.
- W4 compares with W3, W2 and W1.
- W1 has no signal.
- high-side exactly-one hunt becomes sell on the clean symbol.
- low-side exactly-one hunt becomes buy on the clean symbol.
- if buy and sell appear in the same check candle, the check is marked ambiguous/forgotten.

For selected paper entries on the chart symbol, the renderer draws:

- entry text at the next check-candle open;
- SL line at the selected reference W level;
- TP line at Final Reward R;
- entry guide line;
- W4 partial marker for M1 and M2 entries.

## Drawing audit CSV

Level 13 adds:

`stc_level13_drawing_audit.csv`

Columns:

- server write time;
- strategy id;
- run id;
- chart symbol;
- Symbol1;
- Symbol2;
- STC day id;
- New York time;
- M cycle;
- W cycle;
- check index;
- number of drawn objects;
- drawing enabled;
- whether chart symbol supports price layers;
- note.

## Persistence interaction

The drawing layer runs after the Level 12 persistence snapshot/restore pipeline. It does not write to persistence and it does not change persistent trading state.

## Deinitialization

If `InpDrawingClearOnDeinit=true`, Level 13 removes all objects with the configured drawing prefix when the EA is removed.

## Acceptance criteria

Level 13 is accepted when:

1. The EA compiles after adding `DAL_STC_Drawing.mqh`.
2. It still sends no real orders.
3. M/W zones appear on the chart.
4. The 15:30 NY hard-close marker appears.
5. On a Symbol1 or Symbol2 chart, closed W high/low levels appear.
6. Recent SMT/paper entry plans appear when data creates valid candidates.
7. Same-check buy/sell ambiguity is visibly marked.
8. A drawing audit CSV is created.
9. Removing the EA clears drawing objects when clear-on-deinit is enabled.
