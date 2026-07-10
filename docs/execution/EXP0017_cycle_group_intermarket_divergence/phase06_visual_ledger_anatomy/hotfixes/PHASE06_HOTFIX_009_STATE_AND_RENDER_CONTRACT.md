# Hotfix009 — State and Render Contract

## Producer contract

The confirmation field must populate these fields for every final-signal candidate:

```text
symbol_a_reference_frontier
symbol_b_reference_frontier
```

For a high-side candidate:

```text
symbol_a_reference_frontier = symbol_a_high_frontier
symbol_b_reference_frontier = symbol_b_high_frontier
```

For a low-side candidate:

```text
symbol_a_reference_frontier = symbol_a_low_frontier
symbol_b_reference_frontier = symbol_b_low_frontier
```

When the frontier filter is disabled, the upstream frontier classifier marks both symbols valid, and the renderer preserves legacy behavior.

## Consumer contract

Before resolving a chart ID or creating any price object, the renderer evaluates:

```text
chart_symbol == symbol_a => require symbol_a_reference_frontier
chart_symbol == symbol_b => require symbol_b_reference_frontier
other symbol            => reject
```

This check applies equally to:

- hunter legs
- clean/protected companion legs
- confirmed states
- optional invalidated double-hunt visuals
- historical backfill
- live closed-candle refresh

## Preserved invariants

- The expert remains the single state producer for both charts.
- The second chart does not require another expert instance.
- Prices are drawn only on their matching symbol scale.
- Confirmation remains closed-candle based.
- Object IDs remain deterministic.
- Cleanup remains prefix-owned and cannot delete unrelated chart objects.
- Historical processing remains oldest to newest.
- `keep_first_visual_for_same_signal_id` behavior remains unchanged.

## Failure behavior

If the second chart is missing and chart opening is enabled, it is opened and receives only new valid objects.

If a configured chart cannot be found or opened, drawing for that chart is skipped; signal calculation and ledger behavior continue.

If verified cleanup cannot remove all owned objects after four passes, the remaining count is logged. The expert does not delete objects outside `EXP0017_P06_`.
