# Visualization API Contract

## Purpose

This document defines the data contract between the Python research backend and the React visual terminal.

Every metric and experiment must describe its visual output using these generic contracts instead of building metric-specific UI components.

---

## Top-Level Response

A replay visualization response should return:

```json
{
  "dataset": {},
  "candles": [],
  "layers": [],
  "tables": [],
  "selection_map": {},
  "inspector": {}
}
```

---

## Dataset Descriptor

```json
{
  "dataset_id": "GOLD:M15:cache:latest",
  "source": "cache",
  "symbol": "GOLD",
  "timeframe": "M15",
  "start_time": "2026-03-27T00:00:00",
  "end_time": "2026-06-12T23:45:00",
  "bars": 5000,
  "timezone": "broker",
  "data_quality": {
    "has_duplicates": false,
    "is_sorted": true,
    "missing_bars": null
  }
}
```

Allowed `source` values:

```text
cache
mt5
experiment_snapshot
validation_snapshot
manual_upload
```

---

## Candle Contract

```json
{
  "id": "candle:1234",
  "index": 1234,
  "time": "2026-06-12T10:15:00",
  "open": 3350.1,
  "high": 3352.5,
  "low": 3348.2,
  "close": 3351.7,
  "volume": 120,
  "spread": 25
}
```

The chart must render candles from this contract only.

---

## Overlay Layer Contract

```json
{
  "layer_id": "M0001:events",
  "label": "M0001 Events",
  "type": "event_windows",
  "visible": true,
  "z_index": 40,
  "opacity": 1.0,
  "objects": []
}
```

Allowed layer types:

```text
markers
horizontal_levels
zones
event_windows
segments
labels
series
annotations
```

---

## Marker Object

```json
{
  "id": "node:LOW:42",
  "kind": "marker",
  "source_ref": {
    "object_type": "structural_node",
    "object_id": "42",
    "metric_id": null,
    "hypothesis_id": "H0001",
    "experiment_id": null
  },
  "time": "2026-06-10T13:30:00",
  "index": 812,
  "price": 3342.7,
  "shape": "arrow_up",
  "label": "LOW L5",
  "visible_from_index": 817,
  "metadata": {
    "node_type": "LOW",
    "L": 5,
    "confirmed": true
  }
}
```

---

## Zone Object

```json
{
  "id": "m0001:event:node42:revisit1:zone",
  "kind": "zone",
  "source_ref": {
    "object_type": "metric_event",
    "object_id": "node42:revisit1",
    "metric_id": "M0001",
    "hypothesis_id": "H0002",
    "experiment_id": "EXP0001"
  },
  "start_index": 900,
  "end_index": 960,
  "lower": 3339.5,
  "upper": 3344.8,
  "visible_from_index": 900,
  "metadata": {
    "node_id": 42,
    "revisit_id": 1,
    "zone_ratio": 0.9
  }
}
```

---

## Event Window Object

```json
{
  "id": "m0001:event:node42:revisit1",
  "kind": "event_window",
  "source_ref": {
    "object_type": "metric_event",
    "object_id": "node42:revisit1",
    "metric_id": "M0001",
    "hypothesis_id": "H0002",
    "experiment_id": "EXP0001"
  },
  "entry_index": 900,
  "exit_index": 960,
  "entry_time": "2026-06-11T08:15:00",
  "exit_time": "2026-06-11T23:15:00",
  "visible_from_index": 900,
  "complete_from_index": 960,
  "metadata": {
    "RTV": 1.21,
    "event_length": 18,
    "hunted": false
  }
}
```

---

## Table Contract

```json
{
  "table_id": "M0001:events",
  "label": "M0001 Events",
  "primary_key": "event_id",
  "columns": [
    { "key": "event_id", "label": "Event", "type": "string" },
    { "key": "node_id", "label": "Node", "type": "integer" },
    { "key": "node_type", "label": "Type", "type": "string" },
    { "key": "revisit_id", "label": "Revisit", "type": "integer" },
    { "key": "RTV", "label": "RTV", "type": "number" }
  ],
  "rows": []
}
```

A table row must include a `selection_ref`:

```json
{
  "event_id": "node42:revisit1",
  "node_id": 42,
  "node_type": "LOW",
  "revisit_id": 1,
  "RTV": 1.21,
  "selection_ref": {
    "target_type": "event_window",
    "target_id": "m0001:event:node42:revisit1"
  }
}
```

---

## Selection Map

```json
{
  "node:42": {
    "chart_object_ids": ["node:LOW:42", "m0001:event:node42:revisit1:zone"],
    "table_refs": ["M0001:events:node42:revisit1"],
    "inspector_ref": "node:42"
  }
}
```

Selection must be deterministic and bidirectional.

---

## Inspector Payload

```json
{
  "inspector_id": "m0001:event:node42:revisit1",
  "title": "M0001 Event — Node 42 / Revisit 1",
  "sections": [
    {
      "title": "Identity",
      "fields": [
        { "label": "Metric", "value": "M0001" },
        { "label": "Node", "value": 42 },
        { "label": "Revisit", "value": 1 }
      ]
    },
    {
      "title": "Statistics",
      "fields": [
        { "label": "RTV", "value": 1.21 },
        { "label": "Mean Inside", "value": 0.42 },
        { "label": "Mean Before", "value": 0.35 }
      ]
    }
  ]
}
```

---

## M0001 Required Visual Export

M0001 must eventually provide an adapter that maps metric output rows into:

```text
structural node markers
territory zones
event windows
hunt markers
RTV labels
event table
node revisit table
selected event inspector
```

The metric itself should not import UI code.

The adapter lives in `apps/api/app/services/visualization_mapper.py` or a metric-specific mapper under the API layer.

---

## Versioning

Every visualization payload must include:

```json
{
  "contract_version": "ui.visualization.v1"
}
```

Breaking changes require a new version.
