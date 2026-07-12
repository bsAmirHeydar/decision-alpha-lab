# F2 Waist Limit — Performance Contract

## Dedicated executable

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

## Runtime reductions

- Runs once per new chart bar.
- Scans only F1 and F2; F3 construction is disabled.
- Does not run Hook Phase 02.
- Does not build Hook trade snapshots.
- Does not draw chart objects.
- Does not export CSV.
- Does not load production UI, license, release, validation or AI layers.
- Skips the complete detector whenever a managed pending order or position already exists because SL/TP are broker-managed.

## Profiles

### FAST

```text
800 closed bars
scales 2, 3, 5
1800 event/hook caps
```

### PARITY

```text
5000 closed bars
scales 2, 3, 5, 8, 13, 21, 34, 55
6000 event/hook caps
```

FAST changes the historical/scale search envelope, not the F1/F2 or price-rule implementation. Final evidence must be reproduced with PARITY.
