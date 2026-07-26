# UI Folder Structure

## Target Project Layout

```text
decision-alpha-lab/
├── apps/
│   ├── README.md
│   ├── api/
│   │   ├── README.md
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── core/
│   │   │   │   ├── config.py
│   │   │   │   └── paths.py
│   │   │   ├── schemas/
│   │   │   │   ├── market.py
│   │   │   │   ├── nodes.py
│   │   │   │   ├── metrics.py
│   │   │   │   ├── replay.py
│   │   │   │   └── visualization.py
│   │   │   ├── routers/
│   │   │   │   ├── health.py
│   │   │   │   ├── market.py
│   │   │   │   ├── nodes.py
│   │   │   │   ├── metrics.py
│   │   │   │   ├── experiments.py
│   │   │   │   └── replay.py
│   │   │   ├── services/
│   │   │   │   ├── market_service.py
│   │   │   │   ├── node_service.py
│   │   │   │   ├── metric_service.py
│   │   │   │   ├── replay_service.py
│   │   │   │   └── visualization_mapper.py
│   │   │   └── adapters/
│   │   │       ├── market_data_engine_adapter.py
│   │   │       ├── structural_nodes_adapter.py
│   │   │       └── metrics_adapter.py
│   │   └── tests/
│   │       ├── test_health.py
│   │       ├── test_market_contracts.py
│   │       └── test_visualization_contracts.py
│   │
│   └── web/
│       ├── README.md
│       ├── package.json
│       ├── index.html
│       ├── vite.config.ts
│       ├── tsconfig.json
│       └── src/
│           ├── app/
│           │   ├── App.tsx
│           │   ├── routes.tsx
│           │   └── providers.tsx
│           ├── pages/
│           │   ├── LabHomePage.tsx
│           │   ├── ReplayPage.tsx
│           │   ├── MetricsPage.tsx
│           │   ├── ExperimentsPage.tsx
│           │   └── ValidationPage.tsx
│           ├── features/
│           │   ├── replay/
│           │   ├── metrics/
│           │   ├── experiments/
│           │   ├── registry/
│           │   └── inspector/
│           ├── components/
│           │   ├── layout/
│           │   ├── chart/
│           │   ├── tables/
│           │   ├── controls/
│           │   └── primitives/
│           ├── lib/
│           │   ├── apiClient.ts
│           │   ├── queryClient.ts
│           │   ├── time.ts
│           │   └── format.ts
│           ├── types/
│           │   ├── market.ts
│           │   ├── nodes.ts
│           │   ├── metrics.ts
│           │   ├── replay.ts
│           │   └── visualization.ts
│           └── state/
│               ├── selectionStore.ts
│               ├── replayStore.ts
│               └── layoutStore.ts
│
├── docs/
│   └── ui/
│       ├── README.md
│       ├── ARCHITECTURE.md
│       ├── FOLDER_STRUCTURE.md
│       ├── VISUAL_REPLAY_PROTOCOL.md
│       ├── VISUALIZATION_API.md
│       └── ROADMAP.md
│
└── lab/
    └── existing research engine
```

---

## Frontend Feature Boundaries

### `features/replay`

Owns:

- replay controls
- replay speed
- cursor position
- frame stepping
- viewport synchronization

Does not own:

- metric calculation
- node detection

---

### `features/metrics`

Owns:

- metric run selector
- metric parameter display
- metric event table
- metric overlays received from API

Does not own:

- metric computation

---

### `features/experiments`

Owns:

- experiment list
- experiment details
- run status
- experiment outputs

Does not own:

- experiment execution logic

---

### `features/registry`

Owns:

- observation tree
- hypothesis tree
- experiment linkage
- validation linkage
- production signal linkage

---

### `features/inspector`

Owns:

- selected object details
- selected candle details
- selected event details
- selected node details
- source traceability

---

## Naming Conventions

React components:

```text
PascalCase.tsx
```

Hooks:

```text
useSomething.ts
```

API functions:

```text
getSomething.ts
runSomething.ts
```

Types:

```text
SomethingDto
SomethingViewModel
SomethingVisual
```

Backend schemas:

```text
SomethingRequest
SomethingResponse
SomethingDto
```

---

## Rule

If a future metric requires a new chart behavior, add it to the shared visualization protocol first.

Do not hard-code metric-specific visual behavior inside a page component.
