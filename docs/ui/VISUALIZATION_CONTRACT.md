# Visualization Contract

Every test, metric, or experiment must output a common visual contract.

## Required sections

```text
dataset
entity
candles
overlay_layers
tables
stats
timeline
validation_flags
```

## Overlay objects

Supported object kinds:

```text
zone
event_window
segment
marker
label
```

## Synchronization rule

Every visual object must be linkable to a table row or inspector payload by ID.

Example:

```text
chart hover object → highlight table row
table hover row → highlight chart object
click object → select row and jump replay cursor
```
