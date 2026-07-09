# CH08 — Research Translation and Statistical Mission

## 1. What Chapter 08 Turns Into Research

Chapter 08 gives several research obligations.

The strategic answers define candle-close confirmation as important, uniform, and permission-generating. But they do not yet prove its statistical superiority. Therefore, the research mission is to measure the behavior of confirmed divergences after close.

## 2. Primary Research Questions

### 2.1 Does close-confirmed divergence outperform raw hunt observation?

The base strategy requires close confirmation. The research layer should still be able to compare:

- raw hunt moment,
- candle close confirmation,
- post-confirmation movement,
- invalidation after confirmation.

This does not change the doctrine. It measures its quality.

### 2.2 Does waiting for close reduce false divergence?

Because candle close is not considered late, statistics should show whether close confirmation improves:

- win rate,
- expectancy,
- movement quality,
- lower invalidation,
- cleaner trade sequences,
- lower noise.

### 2.3 Are some confirmation candles better than others?

The base strategy does not differentiate confirmation candle types. Later study may discover families:

- close near high,
- close near low,
- large-range confirmation candle,
- small-range confirmation candle,
- confirmation after fast hunt,
- confirmation after slow hunt,
- confirmation near cycle end,
- confirmation early in cycle.

These are not filters yet. They are possible research labels.

### 2.4 Does simultaneous/double hunt behave differently as a non-trade condition?

Double hunt invalidates divergence. But double hunts may still carry market information.

Research can study:

- whether double hunt often causes continuation,
- whether double hunt often exhausts movement,
- whether double hunt differs by CG,
- whether double hunt during cash session behaves differently,
- whether double hunt after one-sided divergence has warning value.

## 3. Recommended Statistical Fields

Chapter 08 implies the following fields should eventually be observable in the research table:

| Field | Meaning |
|---|---|
| `confirmation_time` | The time the active candle closed and the divergence became confirmed. |
| `hunt_time` | The first observed time the hunter touched or passed the reference. |
| `confirmation_delay` | Time between hunt and confirmation. |
| `is_confirmed` | Whether asymmetry survived until candle close. |
| `is_invalidated_before_confirmation` | Whether the clean symbol hunted before confirmation. |
| `is_invalidated_after_confirmation` | Whether the clean symbol later hunted after confirmation. |
| `double_hunt_same_window` | Whether both symbols hunted inside the same decision window. |
| `confirmation_candle_range` | Size of the confirmation candle. |
| `confirmation_position_in_cycle` | Whether confirmation happened early, middle, or late in the CG cycle. |
| `trade_permission_time` | Time at which the strategy had permission to trade. |
| `movement_after_confirmation` | Post-confirmation movement quality. |
| `time_to_invalidation` | If invalidated, how long it survived. |

These names are research labels, not strategy-architect language.

## 4. Outcome Families

A confirmed divergence can later fall into one of several outcome families:

### 4.1 Confirmed and expands

The clean symbol moves in the expected direction after confirmation.

### 4.2 Confirmed and stalls

The divergence confirms but does not produce meaningful movement.

### 4.3 Confirmed and invalidates quickly

The clean symbol hunts after confirmation and destroys the asymmetry.

### 4.4 Invalidated before confirmation

The hunter starts the event, but the clean symbol hunts before the candle closes. No valid divergence remains.

### 4.5 Double hunt in same window

Both symbols hunt the reference level in the same decision window. This is not a divergence.

## 5. Statistical Mission

Chapter 08's statistical mission is:

> Measure whether candle-close-confirmed divergences create a better decision boundary than raw intrabar hunts, while preserving the doctrine that close confirmation is the base permission point.

The strategy wants to know:

- whether close confirmation is enough,
- whether it is too permissive,
- whether some confirmation contexts are better,
- whether invalidation patterns are predictable,
- whether confirmation timing inside the cycle matters,
- whether all confirmed signals should remain tradable,
- whether later portfolio rules should limit simultaneous confirmed signals.

## 6. Statistical Neutrality

Even though candle close is strategically important, the research layer should not assume:

- all close-confirmed signals are profitable,
- close confirmation always improves performance,
- faster confirmation is better,
- slower confirmation is worse,
- late-cycle confirmation is weaker,
- cash-session confirmation is always superior,
- double hunts are useless as market information.

All of this must be discovered.

## 7. Research Law

> Confirmation is the base permission point; statistics decide which confirmation families deserve more trust later.
