# Quant Lab API

## Purpose

The API is the controlled bridge between the Python research lab and the React visual terminal.
It exposes candles, structural nodes, metric events, experiments, validations, and replay payloads through typed contracts.

It does not own research logic.

---

## Current Implementation

The first implemented visual target is:

```text
M0001 — Relative Territory Volatility
source=cache
symbols=GOLD,#US30
timeframe=M15/M1
L=5
zone_ratio=0.9
exit_gap=6
consumption_mode=hunt
```

The API builds a single visualization contract by calling the existing lab stack:

```text
Cache parquet candles
    ↓
CacheMarketDataEngine.get_df()
    ↓
LRuleNodeDetector.detect()
    ↓
M0001RTV.compute()
    ↓
ReplayPayload contract
```

---

## Run

From the repository root:

```powershell
py -m pip install -r apps/api/requirements.txt
py -m uvicorn apps.api.main:app --reload --host 127.0.0.1 --port 8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

OpenAPI docs:

```text
http://127.0.0.1:8000/docs
```

M0001 replay payload:

```text
http://127.0.0.1:8000/replay/M0001?symbol=GOLD&timeframe=M15&L=5&zone_ratio=0.9&exit_gap=6&consumption_mode=hunt&source=cache
```

---

## Endpoints

```text
GET /health
GET /datasets
GET /replay/M0001
GET /metrics/M0001/summary
```

---

## Service Boundaries

```text
routers/      HTTP endpoints only
schemas/      request and response contracts
services/     orchestration and mapping to visualization contracts
adapters/     cache/live adapters with lab-compatible interfaces
core/         config, paths, timeframe helpers
```

---

## Rule

If a value appears on the chart, the API must be able to explain where it came from.

Every response preserves:

```text
source
symbol
timeframe
parameters
contract_version
source_ref for each visual object
selection_ref for linked table rows
```
