# Quant Lab Web Terminal

## Purpose

The web app is the visual research terminal for Decision Alpha Lab.

It must provide a professional replay environment where candles, structural nodes, metric events, hypotheses, experiments, validations, and execution evidence can be inspected together.

---

## Recommended Stack

- React
- TypeScript
- Vite
- TanStack Query
- Lightweight Charts
- ECharts or Plotly for statistical panels

---

## Core Screens

```text
Lab Home
Replay
Metrics
Experiments
Validation
Monitoring
Settings
```

---

## Central Replay Layout

```text
Top navigation
Left research lineage tree
Center candlestick replay
Right object inspector
Bottom dynamic data table
```

---

## Frontend Rule

The frontend displays research truth.
It does not create research truth.

No React component may independently calculate:

- structural nodes
- event validity
- RTV values
- validation status
- signal approval

All of those must come from the API.

---

## First Target

The first real visual target is M0001:

```text
GOLD M15
#US30 M15
L=5
zone_ratio=0.9
exit_gap=6
consumption_mode=hunt
```

The UI must show:

```text
candles
confirmed L-rule nodes
node territories
M0001 event windows
RTV labels
hunt markers
event table
selected event inspector
```
