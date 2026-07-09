# 02 — State Machine

Stage 07 uses key-based state rather than a complex mutable per-event enum.

## State key

```text
event.id + "_" + stage
```

## Stages

```text
PRE_60M
PRE_30M
PRE_15M
PRE_5M
PRE_1M
RELEASE
ACTUAL
BREAKING
```

## Why key-based state

A key ledger is safer than mutating events because the event store may be rebuilt during refresh. If the same event returns from the source with the same stable id, fired stages remain protected. Later stages can persist this ledger to disk if needed.
