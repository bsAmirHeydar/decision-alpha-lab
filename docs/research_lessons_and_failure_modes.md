# Research Lessons and Failure Modes

This document records the most important lessons learned during the H0004 and H0005 development process.

---

## Lesson 1 — Samples are not live decisions

Completed branch samples are useful for discovery. They are not automatically valid as live decision objects.

The problem is not merely that a sample is convenient. The problem is that a sample usually exists after a full event has completed. If the report then uses that object to infer what would have been known earlier, it may accidentally import future knowledge.

Rule:

> If a report claims live validity, it must prove that every label and decision was knowable before the entry it explains.

---

## Lesson 2 — Same-candle labels are simultaneous

A major failure mode was discovered in H0004: several highs/lows or branch labels may become known on the same candle. A classic sequence can sort them by outcome index, entry index, or ID and accidentally create a fake transition.

Example:

- Candle 1000: reversal label becomes known.
- Candle 1000: continuation label becomes known.

This is not:

- reversal then continuation,
- continuation then reversal.

It is:

- one ambiguous known-time batch.

Rule:

> Same known-time means simultaneous. No transition is allowed inside the batch.

---

## Lesson 3 — Classic H4 overstated regime memory

The classic H4 report showed strong regime persistence. After causal batching, the effect became smaller but did not disappear.

Interpretation:

- The original effect was partially inflated by fake same-candle sequencing.
- The remaining effect is still meaningful and should be studied with atomic no-sample replay.

This is a healthy result: a real research process should reduce overstated edges rather than protect them.

---

## Lesson 4 — Continuation PF without a stop is not trading PF

H0005 continuation originally reported strong realized R and profit factor. Code inspection showed that continuation had no real initial stop. The R denominator was a structural distance used for normalization, while the exit was regime change.

That can be useful as path research, but it is not a trading result.

Rule:

> Continuation performance must be recalculated with explicit risk: ATR stop, structural stop, fixed R, trailing, or another executable policy.

---

## Lesson 5 — Reversal and continuation are different species

Reversal and continuation should not be averaged into one headline result.

Observed behavior:

- Reversal often shows short reaction behavior.
- Reversal may fail when held for full structural targets.
- Continuation often produces larger paths but may go adverse before going favorable.
- Continuation needs wider or adaptive risk models.

Rule:

> H5 reports must separate reversal and continuation families.

---

## Lesson 6 — Debug validators must be promoted into main reports

A debug Expert can prove a contract, but it should not remain the only place where the correct logic exists.

If a debug validator discovers the right live-valid rule, the main hypothesis Expert must adopt it.

This happened with:

- D0010 for H4 atomic no-sample regime audit,
- D0009 for H5 atomic no-sample replay,
- main H4/H5 no-sample unification.

---

## Lesson 7 — Random baselines must be matched to the claim

A random baseline must match the question being asked.

Examples:

- If testing structural path direction, match duration, direction, and opportunity context.
- If testing execution, match risk model, session, volatility bucket, and entry family.
- If testing regime memory, compare against permutation, block shuffle, stratified permutation, and far-lag placebo.

No single random test proves everything.

---

## Lesson 8 — A good report can still be non-tradable

A report may reveal a real market fact but still fail as a trading system.

Examples:

- A node may create volatility but not direction.
- A continuation state may create large MFE but require too much MAE.
- A reversal may react but fail at full target.
- A path-normalized R may look strong but disappear under real stop rules.

The project must separate market fact, alpha signal, and executable strategy.
