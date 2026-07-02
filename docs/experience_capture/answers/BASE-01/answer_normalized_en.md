# BASE-01 — Normalized Interpretation

## Core Claim

The market should not be interpreted as a single fixed state.

Every market snapshot must be evaluated through at least two axes:

```text
Direction axis:
  bullish
  bearish

Context axis:
  Hook
  Rally
```

Therefore, each market state should initially be represented as four parallel interpretations:

```text
bullish + Hook
bullish + Rally
bearish + Hook
bearish + Rally
```

This interpretation must then be repeated fractally across multiple scales:

```text
parent scale
current scale
child scale
```

## Structural Meaning

A market move can be a Rally on one scale while being only a component inside a Hook on a higher scale.

A Rally should not automatically be treated as the final context.

A Hook should not automatically be treated as complete just because a local Rally has formed.

The correct interpretation depends on:

```text
where the current move sits inside the Hook cycle
whether the Hook is closing or still open
whether the Rally has entered valid F-counting
whether the Rally is approaching F3
whether the parent scale supports or overrides the current interpretation
```

## Image 1 Interpretation

Image 1 shows a bearish Rally.

However, the important point is that this bearish Rally may itself be inside a larger Hook.

The Hook cycle has not necessarily been completed yet.

The key question is not only:

```text
Is this a bearish Rally?
```

The deeper question is:

```text
Where is this bearish Rally inside the larger Hook?
Is the Hook closing?
Is the Hook still open?
Has the Hook extreme been reached?
Is the market still approaching the Hook's structural destination?
```

So the bearish Rally interpretation remains valid, but it is not sufficient alone. It must be evaluated inside the Hook context.

## Image 2 Interpretation

Image 2 shows a bullish interpretation.

From this view, the first Hook has already closed and the market is now building a Rally.

Inside that Rally, F-counting becomes relevant:

```text
F1
F2
F3
```

The Rally may continue until F3 and then terminate.

However, the same Rally may still be inside a larger Hook. That larger Hook may not even have formed its extreme yet.

The market can still reverse from the current live location. In that case, what looked like a Rally may later be understood as part of a Hook-building process.

Therefore, the system must not collapse too early into one interpretation.

## Required System Behavior

The system must support multi-hypothesis interpretation.

For each market snapshot, it should be able to store and evaluate:

```text
bullish_hook_hypothesis
bullish_rally_hypothesis
bearish_hook_hypothesis
bearish_rally_hypothesis
```

Each hypothesis should have its own:

```text
alive/dead state
quality score
counting state
node context
extreme context
invalidation
destination
fractal support
execution permission
```

## AI Relevance

This experience defines the foundation for the AI architecture.

The AI should not predict one direction directly.

The AI should evaluate multiple structural hypotheses and rank, delay, veto, or route them.

Possible AI layers derived from BASE-01:

```text
Dual Direction Model
Hook/Rally Ambiguity Model
Fractal Context Model
Scenario Ranker
Ambiguity Gate
Execution Router
```

## Feature Families Suggested by BASE-01

```text
direction_hypothesis
context_hypothesis
hook_alive_state
rally_alive_state
hook_cycle_completion_state
rally_f_count_state
parent_context_state
current_context_state
child_context_state
fractal_alignment_state
fractal_conflict_state
hypothesis_quality_score
ambiguity_score
```

## Possible Labels

```text
hypothesis_survived
hypothesis_invalidated
hook_closed
hook_remained_open
rally_completed
rally_failed
f3_reached
parent_context_overrode_current_context
current_rally_was_later_reclassified_as_hook
```

## Execution Consequence

Execution should not be allowed merely because one hypothesis looks attractive.

Before an intent reaches the execution bridge, the system should know:

```text
Which direction hypothesis is being executed?
Which context hypothesis is being executed?
Is the opposing direction still alive?
Is the opposite Hook/Rally interpretation still alive?
Is the parent scale supporting, conflicting, or overriding the current interpretation?
```

## Short Formal Statement

The market must be represented as a fractal multi-hypothesis structure where direction and context remain open until structural evidence resolves them. Execution should be based on ranked and validated hypotheses, not on a single fixed interpretation.
