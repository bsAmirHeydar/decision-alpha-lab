# STAGE 01 — Compile-Safe Core Skeleton Specification

## Product

gartal terminal — MT5 macro-news terminal.

## Stage objective

Build the first production-grade code foundation for the indicator without depending on Forex Factory HTML parsing.

## Scope

### Included

- indicator lifecycle skeleton
- input-to-config mapper
- config validator
- runtime diagnostics
- sample data mode
- event store
- broker GMT detection and conversion primitives
- dashboard shell
- vertical line shell
- bottom timeline shell
- alert state memory
- WebRequest placeholder
- cache placeholder

### Excluded

- production parser
- final luxury UI
- runtime filter buttons
- full timeline projection
- packaging/licensing

## Acceptance criteria

| Area | Requirement |
|---|---|
| Compile | No undefined identifiers in Stage 01 code layer |
| Runtime | Indicator initializes and starts a timer |
| Data | Sample events load by default |
| Dashboard | Shows product header, source status, GMT, counts, next event, and rows |
| Timeline | Shows a bottom shell and vertical lines |
| Cleanup | Removes only prefixed objects |
| Alerts | Alert keys prevent duplicate threshold sends |
| Boundaries | No parser logic inside `GartalTerminal.mq5` |

## Technical decisions

### Data mode

Stage 01 defaults to:

```text
InpUseSampleData = true
```

This maps to:

```text
GT_DATA_MODE_SAMPLE
```

### Object prefix

Default:

```text
GT_
```

Every renderer must derive object names from this prefix.

### Timer discipline

Default refresh:

```text
5 minutes
```

Clamped between:

```text
10 seconds and 3600 seconds
```

### Broker GMT

If auto detection is enabled:

```text
round((TimeCurrent() - TimeGMT()) / 3600)
```

The value is clamped between -12 and +14.

## Engineering gate

Do not begin Stage 02 until Stage 01 has been applied and at least opened in MetaEditor.
