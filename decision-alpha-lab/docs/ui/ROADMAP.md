# UI Implementation Roadmap

## Strategy

Build the UI as a professional research terminal in layers.

Do not start by drawing every possible feature.
Start by building the central replay engine and typed visualization API.

---

## Phase 0 — Architecture Freeze

Deliverables:

- `docs/ui/README.md`
- `docs/ui/ARCHITECTURE.md`
- `docs/ui/FOLDER_STRUCTURE.md`
- `docs/ui/VISUAL_REPLAY_PROTOCOL.md`
- `docs/ui/VISUALIZATION_API.md`
- `docs/ui/ROADMAP.md`
- `apps/README.md`
- `apps/api/README.md`
- `apps/web/README.md`

Definition of done:

- UI purpose is clear.
- Research/UI boundary is clear.
- Replay behavior is specified.
- Visualization contract is metric-agnostic.
- Folder structure is agreed before code is written.

---

## Phase 1 — Backend Read API

Goal:

Expose existing research data to the UI without changing the lab engine.

Endpoints:

```text
GET /health
GET /datasets
GET /market/candles
GET /nodes/l-rule
GET /metrics/M0001/runs
GET /metrics/M0001/events
GET /replay/M0001
```

Definition of done:

- API reads existing parquet cache.
- API can return GOLD M15 and #US30 M15 candles.
- API can return confirmed L-rule nodes.
- API can return M0001 events.
- API can produce `ui.visualization.v1` payloads.
- API tests validate schema and basic row counts.

---

## Phase 2 — Frontend Shell

Goal:

Create the professional terminal frame.

Deliverables:

```text
Top navigation
Left research tree
Center chart area
Right inspector
Bottom dynamic panel
```

Definition of done:

- React app runs with Vite.
- Basic routing exists.
- API client exists.
- Layout is resizable.
- Dark professional terminal theme exists.
- No metric-specific hard coding in layout.

---

## Phase 3 — Market Replay Core

Goal:

Replay candle-by-candle.

Deliverables:

```text
candlestick rendering
play / pause / step controls
speed control
current cursor
viewport control
layer manager
```

Definition of done:

- GOLD M15 cache candles replay correctly.
- Cursor advances by candle index.
- No future candles are visible during replay.
- Replay can jump to selected event.
- Replay state survives simple page refresh through URL/query state.

---

## Phase 4 — M0001 Visual Adapter

Goal:

Visualize the first real metric end-to-end.

Deliverables:

```text
L-node markers
confirmation visibility delay
territory zones
active event windows
completed event windows
hunt markers
RTV labels
event table
selected event inspector
```

Definition of done:

- M0001 events from real cache appear on chart.
- Selecting an event row highlights its chart window.
- Selecting a chart object highlights its table row.
- Inspector shows full M0001 event fields.
- UI visibly distinguishes cache mode from MT5 live sync mode.

---

## Phase 5 — Research Lineage Browser

Goal:

Make observation-to-validation lineage visible.

Deliverables:

```text
Observation list
Hypothesis list
Experiment list
Metric list
Validation list
relationship graph/tree
```

Definition of done:

- H0001 and H0002 are visible.
- M0001 is linked to H0002.
- EXP0001 can be linked to M0001.
- Selecting a research object filters relevant chart artifacts.

---

## Phase 6 — Experiment and Validation Workbench

Goal:

Support comparison, not just replay.

Deliverables:

```text
parameter grid table
run comparison
random baseline comparison
out-of-sample split view
robustness matrix
metric distributions
```

Definition of done:

- Structural vs random baseline can be compared visually.
- Parameter sweeps are explorable.
- Result tables are exportable.
- Validation status is visible and traceable.

---

## Phase 7 — Live Monitor Mode

Goal:

Show current synced market state without compromising research purity.

Deliverables:

```text
live sync status
last candle received
active nodes
active territories
pending events
system health
execution logs when available
```

Definition of done:

- UI clearly marks live mode as non-frozen.
- Current state can be inspected.
- No live-only result is confused with validated research evidence.
