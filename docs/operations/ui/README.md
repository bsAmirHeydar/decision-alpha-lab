# Quant Lab UI Architecture

## Purpose

The Quant Lab UI is the visual operating system for Decision Alpha Lab.

It is not a decorative dashboard.
It is the research cockpit where observations, hypotheses, experiments, metrics, validations, production signals, and execution evidence become visible and inspectable.

The UI must make the full research chain transparent:

```text
Observation
    ↓
Hypothesis
    ↓
Experiment
    ↓
Metric
    ↓
Analysis
    ↓
Validation
    ↓
Production
    ↓
Monitoring
    ↓
Retirement
```

Every visual object must be traceable back to the research object that produced it.

---

## Core Principle

The UI must never become the research engine.

The Python lab remains the source of truth for:

- market data
- structural nodes
- metrics
- experiments
- validations
- reports
- execution logs

The UI only visualizes, navigates, inspects, and controls approved research workflows through explicit APIs.

---

## Product Vision

The central experience is a professional market replay terminal:

```text
Top navigation
    Project stage / symbol / timeframe / experiment selector

Left rail
    Observation → Hypothesis → Experiment → Metric → Validation tree

Center
    Visual Market Replay
    Candles, nodes, territories, events, overlays, annotations

Right inspector
    Selected candle / node / event / hypothesis / metric metadata

Bottom panel
    Dynamic tables, event logs, metric rows, selected object details
```

The UI must feel closer to a research-grade MetaTrader visual tester than a generic analytics dashboard.

---

## Non-Negotiable Requirements

1. The chart must replay candle-by-candle.
2. Every displayed artifact must have a typed source object.
3. Every visual overlay must be toggleable.
4. Selection on chart must synchronize with tables.
5. Selection in tables must synchronize with chart.
6. No UI component may infer market logic locally.
7. All market logic must come from backend contracts.
8. Every experiment visualization must be reproducible from its config.
9. Cached and live market sources must be visibly distinguishable.
10. UI APIs must be generic enough for future metrics, not only M0001.

---

## Recommended Stack

Frontend:

- React
- TypeScript
- Vite
- TanStack Query
- Lightweight Charts
- ECharts or Plotly for statistical panels

Backend:

- FastAPI
- Pydantic schemas
- Parquet cache readers
- Research engine adapters
- Streaming endpoints for replay

Data:

- existing candle parquet cache
- node cache
- metric cache
- experiment reports
- validation outputs

---

## Design Boundary

The UI is allowed to ask:

- show candles
- show nodes
- show M0001 events
- show event details
- replay this run
- select this object
- filter this table
- run this approved test

The UI is not allowed to decide:

- what is a valid node
- when a node is confirmed
- whether an event is valid
- how RTV is computed
- whether a hypothesis is accepted
- whether a signal is production-ready

Those decisions remain in the Python lab.

---

## Document Map

- `ARCHITECTURE.md` — system-level architecture and layer boundaries.
- `FOLDER_STRUCTURE.md` — proposed app and package layout.
- `VISUAL_REPLAY_PROTOCOL.md` — chart, replay, selection, and timeline behavior.
- `VISUALIZATION_API.md` — typed contracts used by metrics and tests to draw on the UI.
- `ROADMAP.md` — staged implementation plan and definition of done.
