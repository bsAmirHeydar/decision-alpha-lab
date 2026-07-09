# CH08 — Candle-Close Confirmation and Trade Permission

## 1. Raw Answers

| Question | Strategy Architect Answer |
|---|---|
| Q1 | Because candle close is very important to me. |
| Q2 | The confirmation candle is the closed candle, and it is important. |
| Q3 | If “same direction” means both symbols hunt the reference level at the same time, the divergence is invalid. |
| Q4 | Yes, the divergence is invalid. |
| Q5 | Only time close. |
| Q6 | No, it is not late. |
| Q7 | No. |
| Q8 | It should be the same. |
| Q9 | Show all of them; all are valid and there is no difference. |
| Q10 | It is trade permission. |

## 2. Chapter Thesis

The strategy separates **hunt occurrence** from **divergence confirmation**.

A hunt can happen the moment price touches or passes a reference high/low. But that is not yet the final decision point. The market is still inside an unfinished candle, and an unfinished candle is not a complete behavioral unit.

The completed candle is the point where the system is allowed to say:

> This asymmetry actually existed at the close of the active decision unit.

This gives Chapter 08 its main doctrine:

> A hunt may be detected during the candle, but the divergence is only confirmed after the candle closes.

## 3. Why Candle Close Matters

Candle close matters because the strategy is not only watching price touch levels. It is watching whether the relationship between two markets remains asymmetric after the active market unit is completed.

Inside an open candle, the market can still change its final meaning:

- the hunter may touch the level and reverse,
- the clean symbol may later hunt too,
- both symbols may end up consuming the reference,
- the apparent divergence may disappear,
- the relationship may stop being asymmetric.

The close does not create the hunt. The close creates the right to judge the hunt.

### Strategic distinction

| Event | Meaning |
|---|---|
| Intrabar hunt | A reference was touched or passed by one symbol. |
| Candle close | The active behavioral unit is complete. |
| Confirmed divergence | The asymmetry survived until the candle close. |
| Trade permission | The strategy may now treat the divergence as actionable. |

## 4. Confirmation Candle Doctrine

The confirmation candle is the candle whose close finalizes the divergence condition.

It is important because it defines the exact boundary between:

```text
Possible divergence
```

and:

```text
Confirmed divergence
```

Before the close, the event is only forming. After the close, it becomes a valid signal candidate.

## 5. Close Is Temporal, Not a Price-Location Filter

The answer “only time close” is crucial.

It means the strategy does not require the candle to close beyond the reference level. It does not ask for a special body condition, rejection candle, displacement candle, or close-confirmed breakout.

The close is used as a time boundary:

> Wait until the candle is finished, then judge whether the divergence still exists.

It is not used as a price filter:

> The candle does not need to close above a high reference or below a low reference to validate the hunt.

### What is required

- The candle must close.
- At the close, one symbol must have hunted the reference.
- The other symbol must not have hunted its corresponding reference.

### What is not required

- No close beyond the reference.
- No rejection pattern.
- No body-size requirement.
- No close-location rule.
- No candle-color rule.
- No displacement requirement.
- No manual visual confirmation beyond the base asymmetry.

## 6. Waiting for Close Is Not Late

The strategy architect explicitly states that waiting for candle close is **not late**.

This is a major philosophical point.

Some strategies view candle-close confirmation as delay. This strategy views it as permission.

The goal is not to capture the first possible tick after the hunt. The goal is to only act after the behavioral unit has completed and the asymmetry is still alive.

### Interpretation

| Impulse View | Chapter 08 View |
|---|---|
| Enter as soon as price touches. | Wait until the candle confirms the relationship. |
| Early entry is better. | Permission is more important than speed. |
| Delay is weakness. | Confirmation is structural discipline. |
| The first tick matters most. | The completed behavioral unit matters most. |

## 7. Confirmation Creates Trade Permission

The answer to Q10 is direct:

> It is trade permission.

Therefore, in the base strategy, confirmation does not merely label the chart. It gives the strategy permission to treat the event as tradable.

This does not mean every confirmed divergence must always produce a trade under every future risk regime. Later layers may define portfolio constraints, overlap rules, maximum exposure, or statistical filters. But at the base strategy language level:

```text
Confirmed divergence = trade permission
```

## 8. Strategy-Level Event Model

The full sequence is:

1. A same-day reference exists.
2. One symbol hunts the reference.
3. The other symbol does not hunt its corresponding reference.
4. The active candle closes.
5. The asymmetry still exists.
6. The divergence is confirmed.
7. Trade permission exists on the clean symbol.

## 9. What This Chapter Does Not Do

Chapter 08 does not define:

- which cycle group is better,
- which time of day is better,
- whether close confirmation improves win rate,
- whether early entry would have performed better,
- whether a wick-only close is better than a body close,
- whether one symbol should be prioritized,
- whether some confirmations should be ignored.

All of those are statistical questions for later.

## 10. Strategic Law

> The market is allowed to hunt intrabar, but the strategy is only allowed to believe the divergence after candle close.
