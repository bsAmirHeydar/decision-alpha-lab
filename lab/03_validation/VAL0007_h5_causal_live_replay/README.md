# VAL0007 — H5 Causal Live Replay

This validation replaces path-first H5 interpretation with live-style replay.

## Hypothesis under test

When H0005 has a known regime state at candle `t`, and that state was knowable
using only data up to `t`, do later zone touches or structural breaks produce
positive post-entry movement?

## What is different from old H5 reports?

Old H5 reports can be useful for structural research, but they are not strict
live execution proof.  VAL0007 treats regime confirmation as a time-stamped event
and processes all samples confirmed on the same candle as one batch.

## Simultaneous breaks

If multiple highs/lows are confirmed on the same candle, they do not form a
chronological sequence.  They are simultaneous.  A mixed reversal/continuation
batch is marked ambiguous by default.

## Entry definitions

Reversal:

- regime energy must be REVERSAL;
- live-visible untouched node zones are activated after the regime is known;
- entry only occurs if a future candle touches the zone.

Continuation:

- regime energy must be CONTINUATION;
- live-visible untouched node zones are activated after the regime is known;
- entry occurs if a future candle breaks the zone by close or intrabar mode.

## Measurement

MFE, MAE, fixed-R reward hit, stop hit, same-bar ambiguity, expectancy, and profit
factor are measured after the actual entry trigger only.
