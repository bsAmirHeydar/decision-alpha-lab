# BASE-03 — Normalized Interpretation

## Core Claim

A valid reason is not any market observation.

A valid reason must come from the project's own anatomy.

The primary source of valid reasons is structural counting.

That means:

```text
Rally counting
Hook counting
their interaction
their fractal position
their execution implications
```

Everything outside this anatomy-first framework is treated as irrelevant or noise unless it can be translated back into the structural language of the system.

## What Counts as a Structural Reason

Structural reasons come from the current state of the market inside the project's anatomy.

Main structural reason families:

### 1. Rally-state reasons

```text
Which F are we in?
Where are we inside the current F?
Are we near F1, F2, or F3?
Are we near a terminal part of the current Rally?
```

### 2. Hook-state reasons

```text
Which Hook number are we in?
Is the Hook early or late?
Are we approaching Hook 3 or Hook 4?
Is the first Hook still unhit while the second Hook is forming?
Is the current Hook state making the market prone to Rally?
```

### 3. Combined structural patterns

A signal can come not from one isolated count, but from a combination:

```text
Hook-Hook-Rally
higher-timeframe F3 + lower-timeframe 3-F reversal
post-F1 continuation entry in the correct direction
Extreme entry near structural limit
```

So a structural reason is a reason that emerges from the bounded structural state space of the model.

## What Counts as a Fractal Reason

A fractal reason comes from cross-timeframe interpretation.

The market must be read in a multi-scenario, multi-timeframe way.

That means the validity of a local setup depends on where it sits inside a higher structural context.

Examples of fractal reasons:

```text
higher timeframe is bullish
lower timeframe is finishing a bearish F3
current local weakness is actually an entry opportunity into higher-timeframe strength
```

or:

```text
a local Hook/Hook/Rally pattern is meaningful because it sits in the correct parent context
```

So a fractal reason is not just "the lower timeframe did something."

It is:

```text
the lower timeframe did something meaningful relative to the higher timeframe
```

## What Counts as an Execution Reason

An execution reason is the part of the anatomy that turns a valid structural idea into a tradable setup.

The user answer implies that execution reasons come from the framework's built-in movement constraints.

These constraints make it possible to define:

```text
entry
stop-loss
target
```

Examples:

### 1. Reversal inside higher-timeframe F3

```text
higher-timeframe F3 is present
lower timeframe shows a 3-F reversal structure
entry can be taken against the exhausted lower move
```

### 2. Post-F1 continuation entry

```text
F1 has formed
direction is judged correct
entry can be taken using the framework
stop can sit below the flag waist
```

### 3. Extreme as one entry family

```text
entry near structural extreme
stop behind structural invalidation
target from anatomy-defined destination
```

So an execution reason is not a vague feeling. It is a structural framework that gives exact operational geometry.

## What Counts as Noise

Anything outside the anatomy-based framework is considered noise unless it can be translated into the anatomy.

The answer explicitly rejects:

```text
candle-based games
technical-analysis pattern games
indicator-based signals
generic technical tricks
```

This means things are noise when they are:

```text
not anchored in Hook/Rally counting
not anchored in fractal context
not anchored in scenario structure
not anchored in anatomy-defined invalidation and destination
```

## Examples of Fake or Misleading Reasons

From the answer, fake or misleading reasons are reasons that may look useful on the chart but do not belong to the ontology.

Examples:

### 1. Candle theatrics

```text
single-candle excitement
isolated candlestick formations
reaction to candle shape without structural context
```

### 2. Indicator-driven triggers

```text
RSI-style overbought/oversold logic
moving-average style signals
oscillator-based entries
indicator crossovers
```

### 3. Generic technical storytelling

```text
pattern naming without anatomy
visual technical tricks
direction calls without Hook/Rally/fractal grounding
```

These may appear persuasive, but from this framework they are not valid reasons.

## Signal Frameworks Mentioned in the Answer

The answer explicitly says Extreme is only one entry family.

Other possible signal families include:

```text
Hook-Hook-Rally
Higher-timeframe F3 + lower-timeframe 3-F reversal
Post-F1 directional continuation entry
Extreme entry
other anatomy-derived entry families to be designed later
```

This means the project should not collapse into one entry style only.

Instead, it should build a library of structurally valid entry frameworks.

## Reason Vector Implication

The future `reason_vector` should not be made of generic technical features.

It should be made of anatomy-native features such as:

```text
hook_number
hook_late_state
hook_3_or_4_proximity
first_hook_unhit
second_hook_active
rally_f_index
rally_f_phase
higher_tf_f_state
lower_tf_f_state
higher_tf_lower_tf_relation
entry_framework_type
flag_waist_stop_geometry
extreme_context_state
```

## Short Formal Statement

A valid reason is a Hook/Rally/fractal state fact derived from the project's own anatomy and capable of supporting a scenario, an entry, an invalidation, or a destination. Anything outside this anatomy-native framework is noise unless it can be translated into the same structural language.
