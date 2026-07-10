# Phase 06 Hotfix010 — Logic and Render Contract

## Evidence flow

```text
M1 history availability
→ complete reference-cycle aggregation for SPX and NDX
→ complete current-cycle aggregation for SPX and NDX
→ one-sided hunt classification
→ strict frontier classification with no skipped later gap
→ final signal
→ symbol-local render gate
→ SPX and NDX chart objects
```

No downstream layer may repair missing upstream evidence by assumption.

## Closed interval convention

All cycle boundaries are represented as exclusive end times:

```text
reference interval = [reference_start, reference_end)
current observed interval = [current_start, confirmation_close)
```

Therefore all M1 requests use:

```text
stop_inclusive = end_exclusive - 1
```

The same convention is used for price aggregation and exact visual anchor lookup.

## Complete-data contract

With `InpRequireM1History=true`, `data_ok` means complete interval coverage, not merely that one or more bars were returned.

A partial `CopyRates` response is classified as missing data and cannot participate in:

- hunt state;
- clean-symbol state;
- frontier state;
- final signal construction;
- chart drawing.

## Frontier gap contract

Let reference candidates be ordered oldest to newest. The classifier scans newest to oldest.

If a newer cycle lacks complete dual-symbol evidence:

```text
later_reference_history_gap = true
```

For every older candidate:

```text
symbol_a_frontier = false
symbol_b_frontier = false
pair_frontier = false
```

This is conservative by design. Unknown intervening history cannot prove freshness.

## Final signal contract

`SCGCFinalSignal` now carries:

```text
symbol_a_reference_frontier
symbol_b_reference_frontier
symbol_a_visual_data_ready
symbol_b_visual_data_ready
```

These are independent symbol-local authorities.

## Strict draw contract

With the default strict mode:

```text
InpEnableExtremeFrontierReferenceFilter = true
InpRequireSymbolLocalFrontierForBothSymbols = true
InpRequireM1History = true
```

The renderer requires:

```text
A_data_ready AND B_data_ready
A_frontier AND B_frontier
```

before drawing either chart.

This makes the accepted signal set and visual set host-independent. Running the expert on SPX cannot give NDX a weaker evidence standard.

## Backfill contract

Historical replay is not allowed to finalize while one symbol is cold or partially synchronized.

```text
not ready => wait, log once, retry next pulse
ready => reset confirmation state, clear owned objects on both charts, replay oldest to newest, finalize
```

## Failure behavior

The patch fails closed:

- incomplete interval: no signal;
- missing newer reference interval: no older frontier proof;
- incomplete non-host visual data: no local line;
- incomplete strict pair evidence: no line on either chart.
