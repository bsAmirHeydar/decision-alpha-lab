# H0005 — Directional Memory of Structural Regimes

H0005 asks whether branch-regime memory becomes usable directional/path memory.

The market is not measured by fixed time windows. Direction is tested structurally:

- **Reversal regime:** the path has an X-axis destination. Entry starts at the next structural zone touch. Success means the opposite node/zone destination is touched before invalidation.
- **Continuation regime:** the path has no fixed X-axis target because structural levels are being broken. Entry starts at the break of the last zone, not merely at a node hunt. Exit is the detected regime change.

## Regime source

The source of the regime is configurable:

- `LAST_ONLY` — default; uses the immediately previous branch label.
- `EWMA_CONTEXT` — uses human-eye EWMA branch context.
- `EWMA_CONSENSUS` — accepts only when last branch and context agree.
- `LAST_WITH_CONTEXT_CONFIDENCE` — uses last branch for direction while retaining context diagnostics.

The default is `LAST_ONLY` because earlier quality tests showed that consensus should not be a hard filter for raw direction; it is better as a confidence layer.

## Path exits

MFE and MAE are measured only until the path exit.

- Reversal exits: opposite-zone target, invalidation break, max-bars cap, or end-of-data.
- Continuation exits: regime change, max-bars cap, or end-of-data.

## Metrics

M0005 reports counts, coverage, target success, follow-through success at multiple zone-width multiples, positive net movement, exit reasons, bars/events to exit, mean/median/P90/P95 MFE and MAE normalized by frozen zone width, net movement, and branch comparisons.

## Random and stress checks

M0005 includes two first-order hard diagnostics:

- **Direction-flip stress:** compares actual direction MFE/follow-through to the opposite direction over the exact same entry-to-exit path.
- **Matched random-entry stress:** compares actual path excursions with deterministic random entries matched by path length and direction.

These tests are designed to show whether the structural regime path contains more directional information than a flipped or random-matched path.
