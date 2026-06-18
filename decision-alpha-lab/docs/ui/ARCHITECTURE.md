# UI System Architecture

## Objective

Build a professional, extensible visual research terminal for Decision Alpha Lab while preserving strict separation between research logic and presentation logic.

---

## High-Level Architecture

```text
apps/web  ───────────────┐
React + TypeScript       │
Visual terminal          │
                         │ HTTP / WebSocket / SSE
                         ↓
apps/api  ───────────────┐
FastAPI                  │
Typed UI contracts       │
Research adapters        │
                         ↓
lab/                     ┐
Market data engine       │
L-rule node detector     │
Metrics                  │
Experiments              │
Validation               │
                         ↓
lab/cache_*              ┐
Candles                  │
Nodes                    │
Metrics                  │
Reports                  │
```

---

## Layer Responsibilities

### 1. Frontend — `apps/web`

Responsibilities:

- render the visual lab terminal
- replay candles through time
- display overlays returned by the API
- synchronize chart selections with table selections
- expose filters, toggles, and inspectors
- call backend endpoints through typed clients

Forbidden:

- calculating structural nodes
- calculating metric values
- deciding event validity
- mutating research results without explicit backend action

---

### 2. API — `apps/api`

Responsibilities:

- expose market data to the UI
- expose structural nodes to the UI
- expose metric runs and event rows to the UI
- expose experiment and validation metadata
- normalize research outputs into visualization contracts
- stream replay frames when needed

Forbidden:

- duplicating metric logic outside the lab modules
- creating UI-only interpretations of research outputs
- returning untyped or ambiguous visual payloads

---

### 3. Research Lab — `lab/`

Responsibilities:

- own all market logic
- own all metric logic
- own all validation logic
- produce deterministic output tables
- preserve reproducibility

The lab does not know about React, charts, or layout.

---

### 4. Cache Layer — `lab/cache_*`

Responsibilities:

- store candles
- store detected nodes
- store metric events
- store validation outputs
- provide reproducible snapshots for UI replay

The UI must always display whether a view is sourced from:

```text
cache
live MT5 sync
experiment snapshot
validation snapshot
```

---

## UI Domain Model

The UI should model the research world through these objects:

```text
ResearchObject
├── Observation
├── Hypothesis
├── Experiment
├── MetricRun
├── ValidationRun
├── Signal
├── MonitoringRun
└── ArchiveRecord
```

The visual layer should model chart objects through these objects:

```text
VisualObject
├── Candle
├── Marker
├── HorizontalLevel
├── Zone
├── Segment
├── EventWindow
├── Annotation
├── MetricSeries
└── TableRow
```

A `VisualObject` must always have a `source_ref` pointing back to the research object that produced it.

---

## Central UI Contract

All metrics, tests, and experiments must expose their visual data through a common contract:

```text
DatasetDescriptor
CandleSeries
OverlayLayer[]
TableSpec[]
SelectionMap
InspectorPayload
```

This prevents each metric from building its own UI.

Instead, each metric only provides data to the UI protocol.

---

## Runtime Modes

### Cache Mode

Used for reproducible research inspection.

```text
parquet cache → API → UI
```

### Live Sync Mode

Used when the market data engine refreshes current candles from MT5.

```text
MT5 → MarketDataEngine → cache → API → UI
```

### Experiment Snapshot Mode

Used when replaying a completed experiment exactly as it was run.

```text
experiment config + frozen cache snapshot → API → UI
```

### Validation Mode

Used to compare multiple runs, splits, parameter grids, and robustness checks.

```text
validation outputs → API → UI statistics panels
```

---

## Event Flow

```text
User selects metric run
    ↓
Frontend requests run manifest
    ↓
API loads candles, nodes, metric events
    ↓
API converts them into visualization contracts
    ↓
Frontend renders replay view
    ↓
User selects chart object
    ↓
Selection store updates
    ↓
Bottom table and right inspector update
```

---

## Design Decision

The first implementation should use React + TypeScript + Vite for the frontend and FastAPI for the backend.

Reason:

- React fits a component-based research terminal.
- TypeScript gives strong UI contracts.
- Vite keeps the frontend simple and fast during early development.
- FastAPI keeps the API close to the existing Python research engine.

Next.js should not be introduced until there is a real need for server-side rendering, public routing, multi-user auth, or external deployment complexity.
