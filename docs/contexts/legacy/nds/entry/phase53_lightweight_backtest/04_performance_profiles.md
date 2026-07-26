# Performance Profiles

## FAST — default

```text
bars: 1200
scales: 2, 3, 5, 8
max events: 2500
max hooks: 2500
Hook scan: 1200 bars
```

Use for rapid strategy iteration, order-flow verification, and broad parameter sweeps.

## PARITY

```text
bars: 5000
scales: 2, 3, 5, 8, 13, 21, 34, 55
max events: 6000
max hooks: 6000
Hook scan: 5000 bars
```

Use for comparison against the production expert and final acceptance runs.

## CUSTOM

All bars, scales, caps, and Hook scan depth come from the custom inputs.

## Interpretation

FAST does not simplify the formulas or validity rules. It bounds the structural context. Results that depend on roots outside the FAST window or on scales 13–55 can differ. Such differences are profile differences, not algorithm forks.
