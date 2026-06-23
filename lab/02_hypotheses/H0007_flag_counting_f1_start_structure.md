# H0007 — Flag Counting / F1 Start Structure

H0007 introduces a mechanical grammar for counting the first flag structure, **F1**, from the M0001 known-time structural node stream.

Canonical algorithm README:

```text
docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE.md
```

## Current design lock

F1 is a topology-only object. It is not a trading strategy and makes no win-rate, profit-factor, R-multiple, or execution claim.

The key rules are:

```text
W is the protected waist.
N1 and N2 are the open count nodes.
R12 is only the internal reaction level between 1 and 2.
R12 must stay inside the main second extreme.
Breaking R12 only arms the structure.
Breaking H2/L2 is required for final confirmation.
```

## Bullish summary

```text
H1 -> W -> H2 -> N1 -> R12 -> N2 -> T12 -> CONF
```

Strict topology:

```text
H2 > H1
W < H1
N1 > W
W < N2 < N1
N1 < R12 < H2
T12 = break above R12
CONF = break above H2
W must survive until CONF
```

Meaning:

```text
R12 must be below H2.
If R12 reaches or breaks H2 before valid N2 exists, this is not a clean F1.
```

## Bearish summary

```text
L1 -> W -> L2 -> N1 -> R12 -> N2 -> T12 -> CONF
```

Strict topology:

```text
L2 < L1
W > L1
N1 < W
W > N2 > N1
N1 > R12 > L2
T12 = break below R12
CONF = break below L2
W must survive until CONF
```

Meaning:

```text
R12 must be above L2.
If R12 reaches or breaks L2 before valid N2 exists, this is not a clean F1.
```

## Research status

This is a structural counting hypothesis only. First deliverables are visual audit, raw event export, invalidation/rejection accounting, and random/null comparison readiness.
