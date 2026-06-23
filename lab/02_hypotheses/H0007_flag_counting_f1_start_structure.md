# H0007 — Flag Counting / F1 Start Structure

H0007 introduces a mechanical grammar for counting the first flag structure, **F1**, from the M0001 known-time structural node stream.

The key design lock is:

> F1 is not confirmed by breaking only the internal roof/floor between count node 1 and count node 2. It must also break the main second roof/floor.

Canonical algorithm README:

```text
docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE.md
```

## Bullish summary

```text
H0 -> W -> H2 -> N1 -> R12 -> N2 -> T12 -> CONF
```

Where:

```text
W   = protected waist, must not break
H2  = main second roof, final confirmation level
N1  = first internal low
R12 = roof between N1 and N2, internal trigger only
N2  = second internal low, lower than N1 but above W
CONF = break of H2, not merely break of R12
```

## Bearish summary

```text
L0 -> W -> L2 -> N1 -> R12 -> N2 -> T12 -> CONF
```

Where:

```text
W   = protected waist, must not break
L2  = main second floor, final confirmation level
N1  = first internal high
R12 = floor between N1 and N2, internal trigger only
N2  = second internal high, higher than N1 but below W
CONF = break of L2, not merely break of R12
```

## Research status

This is a structural counting hypothesis only. It makes no trading, profit-factor, win-rate, or execution claim until the detector is visually audited and compared against null models.
