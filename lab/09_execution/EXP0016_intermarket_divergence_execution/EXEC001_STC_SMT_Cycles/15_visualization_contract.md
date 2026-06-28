# 15 - Visualization Contract

## 1. Purpose

Visualization is required for audit, debugging, and human trust. It is not part of the decision engine.

The drawing layer must never change signal logic.

## 2. Chart independence

The EA can run on any chart. Drawings should be placed on the attached chart for audit, but the underlying logic still uses Symbol1 and Symbol2.

Because a single chart can show only one symbol's price scale, drawings should support two modes:

1. Attached-chart mode: draw events related to the chart symbol if it is Symbol1 or Symbol2.
2. Audit-panel mode: draw textual event summaries regardless of chart symbol.

## 3. Drawing object prefix

All objects should use a safe prefix:

- `DAL_STC_EXEC001_`

The renderer may delete and redraw only objects with this prefix.

## 4. Recommended drawings

Cycle drawings:

- STC day boundary markers.
- M cycle background zones.
- W cycle separators.
- Gap zones as no-entry shaded areas.

Level drawings:

- W high and W low per visible symbol.
- Eligible reference W levels.
- Selected reference level highlighted.

SMT drawings:

- Hunt marker on hunted symbol level.
- Clean symbol marker showing non-hunt.
- SMT candidate label.
- Confirmed signal label.
- Rejected signal label with reason.
- Ambiguous buy/sell discarded marker.

Trade drawings:

- Entry line.
- SL line.
- TP line.
- R distance label.
- Final Reward label.
- Partial close marker.
- Hard close marker.
- AMBIGUOUS outcome marker.

State drawings:

- Current M trade count.
- Current M direction lock.
- Entry STC ON/OFF status.
- Hedging ON/OFF status.
- Partial enabled/disabled status.
- Data completeness warning.

## 5. Drawing defaults

The implementation can choose colors and layout without further owner questions.

Recommended defaults:

- Valid buy: green.
- Valid sell: red/tomato.
- Pending/candidate: yellow/gold.
- Rejected: gray.
- Ambiguous: orange.
- Hard close: purple.
- Gap/no-entry: semi-transparent gray if available.

## 6. Drawing density controls

Inputs should include:

- Draw cycles on/off.
- Draw W levels on/off.
- Draw candidates on/off.
- Draw rejected events on/off.
- Draw trades on/off.
- Draw dashboard on/off.
- Max historical days to draw.

## 7. No further strategy questions

Drawing is an implementation detail. It should be designed to support audit and debugging. It should not ask new questions about strategy rules.
