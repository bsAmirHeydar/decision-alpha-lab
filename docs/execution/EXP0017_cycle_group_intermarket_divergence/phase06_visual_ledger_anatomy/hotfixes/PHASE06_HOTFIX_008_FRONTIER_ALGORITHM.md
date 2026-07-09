# Hotfix008 Frontier Algorithm

## Inputs

For each CG and current closed-candle observation:

```text
previous same-day cycles
symbol A high/low for each previous cycle
symbol B high/low for each previous cycle
current cycle high/low for both symbols
```

## High-side algorithm

Initialize:

```text
seen_A_high = none
seen_B_high = none
```

Walk previous cycles from newest to oldest.

For each reference cycle:

```text
A_high_frontier = no_seen_A_high OR reference_A_high > seen_A_high
B_high_frontier = no_seen_B_high OR reference_B_high > seen_B_high
```

Default strict mode requires both:

```text
high_reference_pair_valid = A_high_frontier AND B_high_frontier
```

After classification:

```text
seen_A_high = max(seen_A_high, reference_A_high)
seen_B_high = max(seen_B_high, reference_B_high)
```

## Low-side algorithm

Initialize:

```text
seen_A_low = none
seen_B_low = none
```

Walk previous cycles from newest to oldest.

For each reference cycle:

```text
A_low_frontier = no_seen_A_low OR reference_A_low < seen_A_low
B_low_frontier = no_seen_B_low OR reference_B_low < seen_B_low
```

Default strict mode requires both:

```text
low_reference_pair_valid = A_low_frontier AND B_low_frontier
```

After classification:

```text
seen_A_low = min(seen_A_low, reference_A_low)
seen_B_low = min(seen_B_low, reference_B_low)
```

## Default mode

```text
InpEnableExtremeFrontierReferenceFilter = true
InpRequireSymbolLocalFrontierForBothSymbols = true
InpSuppressNonFrontierReferenceSignals = true
```

This is intentionally strict. Divergence is only built against clean external frontier levels, not internal already-consumed levels.
