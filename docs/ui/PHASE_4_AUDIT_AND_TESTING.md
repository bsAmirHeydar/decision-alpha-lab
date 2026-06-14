# Phase 4 Audit and Testing Upgrade

## Audit findings

1. **Repository hygiene**
   - `__pycache__`, `*.pyc`, `node_modules`, `dist`, `tsconfig.tsbuildinfo`, temporary patch zips, and generated cache artifacts were appearing in `git status`.
   - Fix: `.gitignore` now explicitly excludes generated Python, frontend, and temporary UI patch artifacts.

2. **Data workflow gap**
   - The UI could visualize cached data but did not expose a first-class fetch/verify data action.
   - Fix: `/api/data/fetch` verifies cache or fetches through MT5 when available.

3. **Chart inspection gap**
   - The chart used crosshair visuals but did not show a TradingView-like time/price readout under the mouse.
   - Fix: chart crosshair now shows a live price label, time label, and compact readout panel.

4. **Metric visualization clarity**
   - M0001 layers were visible, but the UI did not support a direct baseline comparison on the same chart.
   - Fix: actual structural-node M0001 layers and random-baseline M0001 layers can be toggled independently.

5. **Random baseline missing**
   - There was no button to run the same metric logic on random reference points.
   - Fix: `Deep Random Test` generates random candidate points, runs the same RTV event extraction logic, returns overlays/tables/stats, and compares actual vs random.

6. **Hunt marker accuracy**
   - Hunt markers were previously visualized at event exit or by approximation.
   - Fix: the visualization adapter resolves the first candle where the node price is actually hunted and places the marker at that candle and breach price.

7. **Build stability**
   - Old components in `src/components` referenced older type names and `lucide-react`.
   - Fix: backward-compatible type aliases were added and `lucide-react` is explicitly listed.

## New API routes

```text
GET  /api/data/datasets
POST /api/data/fetch
GET  /api/visualizations/m0001
POST /api/visualizations/m0001/random-baseline
```

## UI changes

- Data fetch panel: symbol, timeframe, bars, source.
- Metric controls: L, zone ratio, exit gap, mode.
- Deep Random Test button.
- Clear Random button.
- Actual/random stats comparison cards.
- Actual/random overlay layer controls.
- TradingView-style cursor price/time labels.
- Exact hunt markers.

## Validation performed

```text
pytest: 7 passed
frontend build: passed
```
