# Phase 08 — Limits and Non-Goals

## Limits

Phase 08 depends on the quality of Phase 07 CSV output. If Phase 07 output is missing fields, Phase 08 will treat missing values as zero or empty.

The current CSV parser is deliberately simple. It expects normal comma-separated fields and is not intended for complex quoted text payloads.

## Non-Goals

Phase 08 does not:

```text
trade
execute
place stops
place targets
rank live signals
filter CGs
change risk
mutate strategy
train AI
optimize parameters
```

## Intended Use

Phase 08 exists to reveal statistical structure:

```text
which CGs have better historical behavior
which direction performs better
which role pair performs better
which buckets have bad stop streaks
which buckets are statistically weak
```

The report is evidence, not command authority.
