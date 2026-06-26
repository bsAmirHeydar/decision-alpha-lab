# EXP0016 Antifragile Astro Learning Doctrine

This document defines the thinking style of the Astro ML system. The goal is not to build a complicated astrology predictor. The goal is to build a skeptical learning machine that extracts durable principles from mechanical astro features and market outcomes.

## 1. Core identity

The learner is not a rule collector. It is a principle reducer.

It must prefer:

- principles over details
- fewer assumptions over more assumptions
- out-of-sample survival over in-sample beauty
- broad regimes over tiny special cases
- multi-hypothesis thinking over forced buy/sell labels
- memory with doubt over memory with confidence theater

The correct failure mode is to say:

> I do not know yet. The evidence is not stable.

That is better than memorizing a fragile pattern.

## 2. The main philosophical rule

The model should become antifragile by being exposed to many regimes, many time windows, and many failed hypotheses.

A pattern is not knowledge because it worked in train. A pattern becomes usable knowledge only when it survives:

1. chronological out-of-sample testing,
2. enough sample support,
3. train/test stability,
4. baseline comparison,
5. simplicity pressure,
6. concept-level interpretation.

## 3. The learner must think in principles

A mechanical feature like `t_jupiter_natal_mars_trine_score` is not the final object of learning.

The learner first asks:

- Is this part of benefic expansion?
- Is this part of malefic pressure?
- Is this lunar timing?
- Is this natal activation?
- Is this aspect tension?
- Is this market-quality timing?

Then it asks whether the broad concept has durable predictive value.

Only if the broad concept is stable may the system inspect the detail.

## 4. The learner must think in multiple possible market outcomes

The market does not only go up or down. The same astro condition may mean different behavioral outputs:

- direction up
- direction down
- flat/no edge
- clean long path
- clean short path
- spike/hunt
- bull trap
- bear trap
- noisy no-trade

Therefore the learner should never force every astro condition into BUY or SELL.

A good learning result may be:

> This does not predict direction, but it predicts spike risk.

or:

> This does not produce short direction, but it invalidates long continuation.

## 5. The learner must be reductive, not additive

The system must resist the temptation to add conditions endlessly.

Bad learning style:

> If Jupiter is high, and Moon is in this bucket, and Saturn is below this threshold, and the hour is this, and the third decimal of some score is this, then buy.

Good learning style:

> Benefic expansion alone is not directional. It becomes dangerous when exhaustion is high and malefic pressure rises. Treat it as bull-trap risk, not buy confirmation.

## 6. The learner must punish complexity

Every extra condition must pay rent.

A complex model is allowed only when it adds out-of-sample value after complexity penalty.

The default hierarchy is:

1. baseline / majority class
2. single broad concept rules
3. shallow tree
4. sparse logistic model
5. small forest
6. extra trees challenger
7. neural challenger

The neural model is never automatically trusted. It is a challenger, not an oracle.

## 7. The learner must keep a skeptical memory

Memory has three layers:

### Case memory

Historical situations:

- timestamp
- astro signature
- prediction
- actual outcome
- success/failure
- closest similar past cases

### Concept memory

Stable concept families:

- benefic expansion
- malefic pressure
- lunar timing
- natal activation
- aspect tension
- market quality

### Principle memory

Only accepted rules:

- sufficient train support
- sufficient OOS support
- positive train lift
- positive OOS lift
- low train/test gap

Rejected rules are also stored. They are useful because they tell us what not to believe.

## 8. The anti-overfit gate

A rule is rejected if any of these are true:

- low train support
- low OOS support
- weak train lift
- no OOS lift
- unstable train/test gap
- no edge over baseline
- excessive complexity

Rejected knowledge must remain visible. The goal is not to hide failure; the goal is to learn from failure.

## 9. Neural networks are allowed only under discipline

Deep learning may be useful when the system has enough data and when sequence effects matter.

But neural models are dangerous because they can memorize beautifully.

A neural challenger is only useful if:

- train/test gap is controlled,
- OOS edge beats simpler models,
- probability calibration is acceptable,
- its predictions can be summarized by stable concepts or case memory,
- it survives walk-forward testing.

If a neural model wins only in train, it is not intelligence. It is decoration.

## 10. Production meaning

This learner should not directly trade at first.

Its first production role is regime interpretation:

- prefer long
- prefer short
- avoid long
- avoid short
- expect spike
- expect trap
- no clean edge

Only after OOS durability should any output become an execution filter.

## 11. Final doctrine

The best astro learner is not the one that finds the most patterns.

The best astro learner is the one that rejects the most false patterns while preserving a small number of durable principles.

## The Learner's Known Cognitive Fragilities

The antifragile layer assumes that the learner is always vulnerable to several predictable thinking failures:

1. **Single-split luck** — a pattern can survive one train/test split only because the chosen boundary was favorable.
2. **Condition creep** — adding more rules can make the system look smarter while actually making it more brittle.
3. **Concept monoculture** — a model can depend on one broad concept family and collapse when that family changes regime.
4. **Numeric perturbation sensitivity** — a model that changes its decision under tiny feature noise is not robust enough to become knowledge.
5. **Contradictory interpretation** — the same concept/state can appear to support both UP and DOWN, or clean long and clean short, if the learner is not forced to reconcile hypotheses.
6. **Support illusion** — a high lift from a tiny sample is not knowledge; it is a research lead.
7. **Neural overconfidence** — a neural challenger can discover useful nonlinear structure, but it can also memorize noise. It is never accepted unless it survives the same OOS and fragility gates as simpler models.

## The Hardening Rule

The learner now has three knowledge levels:

- **Pattern**: something statistically interesting inside one run.
- **Candidate principle**: a pattern that survived the first antifragile gate.
- **Hardened principle**: a candidate principle that also survived temporal fold stress, perturbation stress, dependency stress, contradiction audit, and condition-creep audit.

Only hardened principles are allowed to move toward production logic, MQL filters, or reusable trading doctrine.

## How Antifragility Enters the Logic

The system does not become antifragile by adding more conditions. It becomes antifragile by reducing false knowledge:

- It collapses many mechanical features into broad concept families.
- It tests whether each principle survives across multiple chronological folds.
- It perturbs feature values and checks whether model decisions remain stable.
- It removes one concept family at a time to detect monoculture dependency.
- It flags contradictions between targets and horizons.
- It penalizes rule proliferation.
- It exports hardened principles separately from fragile research leads.

The goal is not to maximize in-sample accuracy. The goal is to produce fewer beliefs, but beliefs that survive damage.
