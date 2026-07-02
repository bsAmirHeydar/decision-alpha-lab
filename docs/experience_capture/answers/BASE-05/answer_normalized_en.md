# BASE-05 — Normalized Interpretation

## Core Claim

Ambiguity is allowed only as a structured multi-hypothesis state.

It is useful when it preserves multiple valid structural interpretations.

It becomes dangerous when the system cannot identify which context has power, where the move originated, what structure limits the move, or which execution side has defined invalidation and reward.

## Ambiguity Is Not Random Uncertainty

The uncertainty described here is not vague confusion.

It is structured uncertainty.

The system must not say:

```text
anything can happen
```

Instead, it must say:

```text
these specific contexts are alive
these contexts have different power levels
these contexts come from different origins
these contexts have different structural limits
these contexts imply different execution routes
```

## Origin of Move

A key addition in BASE-05 is the idea that every current move must be traced back to its origin.

For any Rally or Hook, the system must ask:

```text
Where did this move come from?
Did it come after a completed F3?
Did it come after two Hooks?
Did it come from a parent-scale terminal zone?
Did it come from a parent-scale continuation context?
```

This means the move itself is not enough.

The origin of the move is part of its meaning.

## Position Inside the Origin-Derived Move

The system must also know:

```text
Where are we inside the move?
Where are we inside the larger move created by the origin?
Is the move early, middle, late, terminal, or still open?
```

This is important because the same local pattern can mean different things depending on where it sits inside its origin-derived structure.

## Context Power

The system must learn which context has more power.

Context power must not come from external indicators or generic technical analysis.

It must come from NDS-native reasons:

```text
Hook count
Rally F-count
F3 state
Hook completion state
node state
fractal relationship
origin of move
higher-scale continuation or terminal pressure
```

A context is powerful when its NDS reasons dominate the competing contexts.

## Human-Like Broad View

The desired system must see like a human in the following sense:

```text
it keeps multiple contexts open
it understands where each context came from
it compares their structural power
it tracks parent/current/child relationships
it does not collapse too early into one direction
it knows when to wait for a better base
```

This is not discretionary randomness.

It is a structured multi-context reasoning process.

## Image 1 Interpretation

Image 1 shows the higher timeframe, H1.

In the user's interpretation, the market is showing a bearish F3 on the one-hour timeframe.

A bearish F3 on the higher timeframe can imply that the bearish move is approaching exhaustion or terminal pressure.

Therefore, the higher-energy dominant implication may become bullish.

This does not mean immediate buy.

It means the system should recognize that the higher timeframe may favor bullish continuation or reversal after the bearish F3 context matures.

## Image 2 Interpretation

Image 2 shows the lower timeframe, M10.

If the lower timeframe shows a bullish F3 while the higher timeframe context suggests stronger bullish energy after a bearish F3, the system should not blindly take a sell only because the lower timeframe shows a local bullish F3.

Instead, the system should wait for the market to come down and create a proper base, such as a Hook, where a buy can be taken.

This is a key execution consequence:

```text
do not short a lower-timeframe F3 if higher-timeframe context power favors the opposite side
wait for a better base aligned with the stronger context
```

## Higher-Than-H1 Override

The answer also introduces a larger-scale override.

If a timeframe above H1, such as H4 or Daily, is bearish and is not at F3 or terminal pressure, then the bearish context may still dominate.

In that case, the H1 bullish implication may be limited.

Then, if M10 completes three upward Fs, a sell may become valid because it aligns with the stronger higher-scale bearish context.

So context power is hierarchical:

```text
higher scale can override lower scale
but only through NDS-native structural reasons
```

## Natural and Useful Ambiguity

Ambiguity is natural and useful when:

```text
multiple NDS-valid contexts are alive
each context has identifiable reasons
the origin of each move is known
the structural limits are clear
each side has potential execution geometry
one side may be used for main entry while the other manages risk or protects profit
```

Useful ambiguity supports:

```text
watch mode
delayed entry
ranked scenarios
dual-intent preparation
hedge planning
profit protection
```

## Dangerous Ambiguity

Ambiguity becomes dangerous when:

```text
contexts are not structurally grounded
origin of move is unclear
higher-scale power is unknown
invalidation is not defined
destination is not defined
both sides are only weak stories
execution geometry is not clean
hedge would add cost without protecting profit
```

Dangerous ambiguity should lead to:

```text
NO_TRADE_AMBIGUOUS
WATCH_ONLY
WAIT_FOR_BASE
WAIT_FOR_CONTEXT_RESOLUTION
```

## Ambiguity Scoring vs Classes

The best design is both.

AI should produce a numeric ambiguity score and a class.

Suggested score:

```text
ambiguity_score = 0.00 to 1.00
```

Suggested classes:

```text
STRUCTURED_MULTI_CONTEXT
USEFUL_AMBIGUITY
DOMINANT_CONTEXT_CLEAR
DANGEROUS_AMBIGUITY
NO_TRADE_AMBIGUOUS
WAIT_FOR_BASE
DUAL_INTENT_CANDIDATE
HEDGE_PROTECTION_CANDIDATE
```

The score allows ranking and gradual behavior.

The class allows execution gates to act safely.

## Two-Sided Reward and Hedge

The answer also states that both sides may sometimes be exploited because the framework can provide good reward.

This does not mean random hedging.

It means:

```text
if both sides have valid structural geometry
and if one side has already produced profit
and if the opposite side becomes valid
then hedge can be used to preserve part of the profit
```

This implies a future model:

```text
Hedge Protection Router
```

The hedge logic should be tied to:

```text
profit protection
context shift
dual valid scenarios
defined invalidation on both sides
execution cost
```

## Execution Consequence

The execution bridge should not simply trade the strongest local signal.

It should ask:

```text
Which scale has dominant context power?
Where did the local move originate?
Is the local F3 aligned with or against the higher-scale context?
Should we trade now, wait for a base, or use a hedge to protect profit?
```

## Short Formal Statement

Uncertainty is allowed when it is structured by NDS contexts, move origin, fractal hierarchy, context power, and clear execution geometry. Ambiguity becomes dangerous when those contexts cannot be ranked or when execution cannot be bounded. AI should score ambiguity and classify it into actionable states such as wait, watch, trade, dual-intent, hedge-protection, or no-trade.
