<!-- CURRENT CANON NOTICE
This file is retained as historical/context documentation. For current Phoenix implementation decisions, use:

docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting vNext Implementation Notes

This document maps the v3 concept specification into the first clean MQL5 implementation module.

## 1. Why a vNext module exists

Previous implementations evolved through patches over a pattern scanner. That architecture was not aligned with the final concept:

- Flag counting is fractal.
- Several sequences can be active in parallel.
- A confirmed F1 must spawn the search for F2.
- A confirmed F2 must spawn the search for F3.
- Different swing scales can produce different valid sequences.

The vNext module starts from a clean event model and avoids the old M0007/M0008 path.

## 2. Data model

Each detected structure is an `FCN_Event` with:

- scale level `scale_L`
- sequence id
- parent event id
- chain step
- F level: F1/F2/F3
- direction
- status
- Origin, Leg1, Waist, Leg2
- Internal 1 and Internal 2
- confirmation point
- invalidation point
- body size and parent size
- reason string for audit

## 3. Node engine

For every configured `L`, the engine detects swing highs and lows using an L-left/L-right rule, then compresses consecutive same-kind nodes by keeping the more extreme node.

This creates one node stream per scale.

## 4. F1 logic

F1 core body:

- Bullish: Origin low, Leg1 high, Waist low above Origin, Leg2 high above Leg1.
- Bearish: Origin high, Leg1 low, Waist high below Origin, Leg2 low below Leg1.

F1 post-body rule:

- Internal 1 and Internal 2 must form before confirmation.
- If Leg2 extends before Internal 1/2 complete, the event remains in Leg2 extension and restarts the internal-count search.
- Confirmation happens only after Internal 1/2 and then own Leg2 rebreak.
- Invalidation happens if own Waist breaks before confirmation.

## 5. F2 logic

F2 starts from parent F1 Internal 2.

F2 body uses the same body geometry as F1, but invalidation is different:

- F2 invalidation = break of F2 Origin.
- F2 can break its own Waist without invalidation.
- If Waist breaks, branch labels are `1 = Waist`, `2 = waist-breaking node`.
- F2 can extend Leg2 before later forming Internal 1/2.
- F2 must be at least parent F1 body size by default.

## 6. F3 logic

F3 starts from parent F2 Internal 2.

F3 body uses the same body geometry, but after the two-leg body is complete it is considered terminal for the sequence. Post-F3 movement is special and should be handled by the next research layer. The renderer uses separate terminal colors for F3.

## 7. Rendering

The renderer is deliberately body-only:

- Origin to Leg1: straight trend line.
- Leg1 to Waist to Leg2: smooth curve passing through the Waist.
- Level labels: tiny F1/F2/F3.
- Internal labels: tiny 1/2 only.
- No lines are drawn from Leg2 to 1/2.

Line width and font size increase with larger scale L.

## 8. Inputs

The experiment exposes multiple swing scales and all draw filters. Detailed logs are off by default.

## 9. Next work

The next layer is ND/Hook partitioning:

- detect ND phases where no valid F can form at the current scale,
- adapt L so ND can be represented in three or four high/low nodes,
- mark an ND phase as resolved when the following F1 confirms,
- expose queryable state: in ND or in F, which F level, where inside the sequence.


## Origin identity and live-root display contract

Root display is soft by default. A coherent high/low F1 body may be rendered while it is still live, even before internal `1/2` and confirmation, so the chart does not become artificially empty. Strict root filters remain available for audit/debug through `InpRequireF1Internal12ForRoot` and `InpRequireF1ConfirmedForRoot`, but both default to `false`.

Invalid/orphan structures are not controlled by hiding all live roots. They are controlled by identity invalidation: if the candidate touches or crosses its own Origin / start of leg before completing the relevant body, that candidate is removed and later movement is not attached back to the dead origin.

Each rendered F body keeps a traceable identity through `F#/L#/Q#` labels and an `O` origin label, so the chart shows which flag/scale/sequence owns each body and where its first leg starts. ND remains high/low-node based and close-agnostic.
