# Quant Lab API

## Purpose

The API is the controlled bridge between the Python research lab and the React visual terminal.

It exposes candles, nodes, metrics, experiments, validations, and replay payloads through typed contracts.

It does not own research logic.

---

## Recommended Stack

- FastAPI
- Pydantic schemas
- pandas / pyarrow for parquet reads
- existing `lab/` modules as adapters

---

## Initial Endpoints

```text
GET /health
GET /datasets
GET /market/candles
GET /nodes/l-rule
GET /metrics/M0001/events
GET /metrics/M0001/summary
GET /replay/M0001
```

---

## Service Boundaries

```text
routers/      HTTP endpoints only
schemas/      request and response contracts
services/     orchestration and mapping
adapters/     calls into lab modules
core/         config and paths
```

---

## Rule

If a value appears on the chart, the API must be able to explain where it came from.

Every response should preserve:

```text
source
symbol
timeframe
parameters
run_id or cache path
contract_version
```
