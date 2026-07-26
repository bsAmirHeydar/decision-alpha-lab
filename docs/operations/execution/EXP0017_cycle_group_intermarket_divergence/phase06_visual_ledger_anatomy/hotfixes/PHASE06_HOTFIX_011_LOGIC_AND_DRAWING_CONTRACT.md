# Hotfix011 Logic and Drawing Contract

## Detection contract

For candidate reference `R`, symbol `S`, and current cycle `C`:

```text
path(S, R, C) = M1 bars from R.end inclusive to C.start exclusive
```

High-side freshness:

```text
max(path.high) < R.high
```

Low-side freshness:

```text
min(path.low) > R.low
```

With tick-size normalization:

```text
high consumed when path.high >= R.high - tolerance
low consumed when path.low <= R.low + tolerance
```

An adjacent reference has an empty intervening path and is fresh before the current cycle.

## Pair contract

When `InpRequireSymbolLocalFrontierForBothSymbols=true`:

```text
pair_high_fresh = SPX_high_fresh AND NDX_high_fresh
pair_low_fresh  = SPX_low_fresh  AND NDX_low_fresh
```

Missing evidence is never treated as fresh.

## Signal contract

A final signal carries:

- SPX local reference price;
- NDX local reference price;
- SPX local current extreme;
- NDX local current extreme;
- SPX local reference timestamp;
- NDX local reference timestamp;
- SPX local current-extreme timestamp;
- NDX local current-extreme timestamp;
- local raw-path data readiness;
- local side-specific freshness.

## Drawing contract

A chart leg is authorized only when its own symbol-local fields satisfy:

```text
local reference/current data ready
AND
local raw-path proof ready
AND
local reference fresh for the signal side
```

The renderer uses stored approved anchors. It must not perform an independent source-of-truth calculation for NDX.

## Cleanup contract

Before authoritative historical reconstruction:

```text
bulk delete all EXP0017_P06_* objects on SPX chart
bulk delete all EXP0017_P06_* objects on NDX chart
verify zero remaining owned objects
replay oldest to newest
```

Manual objects without the project prefix remain untouched.
