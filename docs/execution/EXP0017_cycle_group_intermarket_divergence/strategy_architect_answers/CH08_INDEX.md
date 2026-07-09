# CH08 — Candle-Close Confirmation, Invalidation, and Trade Permission Index

## Chapter Identity

Chapter 08 defines the point at which raw divergence becomes a usable signal.

The previous chapters defined the raw world:

- two related symbols,
- a cycle-group container,
- a reference high or low,
- hunt-only behavior,
- clean-symbol asymmetry,
- same-day reference memory,
- neutrality between cycle groups,
- time-window hypotheses.

Chapter 08 answers a different question:

> When is the divergence allowed to exist as a decision-worthy market event?

The answer is:

> The hunt may occur inside the candle, but the divergence is not considered confirmed until the active candle closes.

This chapter is not about adding another price filter. It is about forcing the market to complete the active time unit before the event is accepted.

## Files in This Chapter

1. `CH08_candle_close_confirmation_and_trade_permission.md`
2. `CH08_research_translation_and_statistical_mission.md`
3. `CH08_invalidation_and_simultaneous_hunt_doctrine.md`
4. `CH08_signal_visibility_and_equality.md`
5. `CH08_hypothesis_register.md`
6. `CH08_glossary_and_language.md`

## Core Doctrine

The Chapter 08 doctrine can be reduced to seven strategic laws:

1. **Hunt is intrabar-aware, but confirmation is candle-close-aware.**
2. **The confirmation candle matters because it defines the completed behavioral unit.**
3. **Close confirmation is temporal, not a required close beyond the hunted level.**
4. **If both symbols hunt their corresponding reference, the divergence is invalidated.**
5. **Waiting for candle close is not late; it is the moment of permission.**
6. **All confirmed divergences should be shown and treated as valid before statistics.**
7. **Confirmation creates permission to trade.**

## Connection to Previous Chapters

| Previous Chapter | Connection |
|---|---|
| CH01 | Divergence is the language of behavioral asymmetry. CH08 defines when that language becomes readable. |
| CH02 | Both symbols are valid. CH08 decides whether the relationship is asymmetric or cancelled. |
| CH03 | Hunt is touch-only. CH08 adds the requirement that the active candle must close before the event is accepted. |
| CH04 | References can come from previous same-day cycles. CH08 decides when a current-cycle reference interaction becomes a confirmed signal. |
| CH05 | All cycle groups are independent units. CH08 applies the same confirmation law to every CG. |
| CH06 | All CGs are neutral before statistics. CH08 prevents confirmation rules from favoring one CG before evidence. |
| CH07 | Time windows remain statistically discoverable. CH08 ensures time-based confirmation is consistent across sessions. |

## Strategic Output

After Chapter 08, the base strategy has a clean three-stage event model:

```text
Reference exists
↓
One symbol hunts, the other does not
↓
Active candle closes
↓
Divergence is confirmed
↓
Trade permission exists
```

If the clean symbol also hunts before confirmation or at the same confirmation boundary:

```text
Reference exists
↓
Both symbols hunt their corresponding reference
↓
Asymmetry disappears
↓
Divergence is invalid
↓
No trade permission
```
