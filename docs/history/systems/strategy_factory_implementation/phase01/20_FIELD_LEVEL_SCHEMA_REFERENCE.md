# Field-Level Schema Reference

This document is the operational field catalog for Phase 01. It is intentionally explicit because later adapters must not guess field meaning.

## SchemaIdentity

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `schema_namespace` | ASCII string | yes | Organizational namespace. |
| `schema_name` | ASCII string | yes | Contract name. |
| `major` | int | yes | Incompatible revision counter. |
| `minor` | int | yes | Backward-compatible capability revision. |
| `patch` | int | yes | Compatible correction revision. |

## MarketTimestamp

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `utc_epoch_milliseconds` | signed 64-bit integer | yes | Canonical ordering time. |
| `source_timezone_id` | ASCII string | yes | Source timezone lineage, such as `America/New_York`. |
| `source_utc_offset_minutes` | int | yes | Offset active at source observation time. |
| `source_clock_id` | ASCII string | yes | `broker`, `exchange`, `terminal`, `python`, or versioned feed clock. |
| `precision` | enum | yes | Seconds, milliseconds, or microseconds source precision. |

## BarRecord

`symbol`, `timeframe_seconds`, open/close timestamps, OHLC, tick/real volume, bid/ask close, spread points, source ID, and source bar ID. `bar_id` is derived and must not be manually invented.

## AnatomyEvent

| Field group | Fields | Rule |
|---|---|---|
| Schema | `schema` | Must be compatible with AnatomyEvent 1.x. |
| Identity | `event_id` | Empty during construction or exact derived ID. |
| Strategy | `strategy_id`, `strategy_version` | Stable and versioned. |
| Producer | `producer_id`, `producer_version` | Exact engine/adapter producer. |
| Market | `symbol`, `reference_symbol`, `direction` | Direction cannot be NONE. |
| Causality | `event_time`, `known_time`, `confirmation_time` | Ordered and UTC canonical. |
| Geometry | `reference_price`, `invalidation_price`, `timeframe_seconds` | Finite, positive timeframe. |
| Context identity | `session_id`, `parent_event_id`, `market_event_cluster_id` | Cluster is mandatory. |
| Lineage | `source_hash`, `anatomy_state` | Source hash mandatory; state versioned by producer. |

## FeatureValue

A tagged union. Exactly one semantic value is active according to `value_type`. Quality is separate from type. `known_time` is the first valid availability time of this value, not the snapshot time.

## FeatureSnapshot

The snapshot contains ordered unique feature IDs. `state_generation` identifies the runtime state generation from which the snapshot was compiled. The exact order becomes important later when a model vector schema is compiled.

## ArtifactIdentity

Every materialized artifact carries Git, strategy, producer, manifest, source, run, schema, and creation lineage. No report or model may exist outside this lineage model.
