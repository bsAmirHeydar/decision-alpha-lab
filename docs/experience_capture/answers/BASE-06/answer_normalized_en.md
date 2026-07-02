# BASE-06 — Normalized Interpretation

## Core Claim

The ontology is fixed.

The usage policy is learnable.

This means:

```text
NDS concepts and definitions = hard rules
how to combine, rank, route, and execute them = learnable
```

AI may learn how to use the anatomy, but it may not redefine the anatomy or import concepts from outside it.

## Hard Rules

Hard rules are non-negotiable constraints.

They define the permitted universe of the system.

### Hard Rule 1 — NDS-only reasoning

All reasons, viewpoints, decisions, model inputs, labels, and execution logic must be based only on NDS-native anatomy.

Allowed concept families include:

```text
Hook
Rally
F-counting
Node-counting
X-axis structure
Y-axis state
fractal context
scenario state
invalidation geometry
destination geometry
execution geometry derived from NDS
```

Forbidden concept families include:

```text
indicators
ICT
generic technical analysis
external trading systems
raw candle-pattern logic
artificial time-horizon labels
time-of-day signal logic
day-of-week signal logic
```

### Hard Rule 2 — Hook definitions are fixed

The definition of Hook must not be changed by AI.

AI may score Hook quality or use Hook context, but it may not redefine what Hook is.

### Hard Rule 3 — Rally definitions are fixed

The definition of Rally must not be changed by AI.

AI may evaluate Rally state, Rally maturity, or Rally interaction with other contexts, but it may not redefine Rally.

### Hard Rule 4 — Counting definitions are fixed

F-counting and Node-counting are part of the core anatomy.

AI may learn which count states are more useful, dangerous, terminal, or executable, but it may not rewrite the counting system.

### Hard Rule 5 — No external decision ontology

AI cannot introduce external explanations such as:

```text
RSI is oversold
ICT liquidity sweep happened
moving average crossed
price broke a trendline
this is a classical support/resistance bounce
```

If an external-looking observation cannot be translated into NDS language, it must be rejected.

## Learnable Layers

The learnable layer begins after the NDS state is built.

AI can learn how to use NDS states.

Learnable areas include:

```text
which scenario has more power
which context dominates
which fractal scale should have more weight
when ambiguity is useful
when ambiguity is dangerous
when to wait for a base
when to use an Extreme entry
when to use a post-F1 continuation entry
when to use a lower-timeframe reversal inside higher-timeframe F3
when to cancel or replace a pending order
when dual-intent or hedge-protection is allowed
```

In short:

```text
The concepts are fixed.
The policy over the concepts is trainable.
```

## Feature Examples

A feature is a measurable NDS-native state that AI can learn from.

Examples:

```text
hook_number
hook_late_state
rally_f_index
f3_terminal_candidate
node_unreached_state
parent_context_power
current_context_power
child_trigger_quality
fractal_alignment_state
ambiguity_score
scenario_quality
execution_readiness_state
spread_to_risk_ratio
```

These are allowed because they are either NDS-native or execution-cost geometry attached to NDS execution.

## Test-Only Examples

Some claims should not become hard rules immediately.

They should become hypotheses and be accepted only after testing.

Examples:

```text
A lower-timeframe bearish F3 inside a bullish higher-timeframe context creates a good buy opportunity.
Hook-Hook-Rally is a valid signal family.
Post-F1 continuation entry works when direction is correct.
A local F3 should be ignored when higher-timeframe context power dominates.
Dual-intent can improve reward capture.
Hedge-protection can preserve profits without destroying expectancy.
```

These are not ontology definitions.

They are policy or edge claims.

Therefore, they must be tested.

## If AI Gets a Better Result Than Experience

AI may be accepted only under strict conditions.

It cannot violate hard ontology rules.

AI can disagree with experience only inside the learnable policy layer.

Acceptance conditions:

```text
the model uses only NDS-native inputs
the model does not import forbidden concepts
the model beats rule-based baselines
the result survives out-of-sample testing
the result survives structural OOS testing
the result passes negative controls
the result passes ablation tests
the model has an interpretable reason vector
the improvement is not caused by leakage
the improvement is stable across relevant regimes or clearly documented niche conditions
```

If AI violates NDS ontology, the result is rejected even if the backtest looks better.

If AI stays inside NDS and improves how NDS concepts are used, the result can be accepted.

## AI Boundary

The correct AI role is:

```text
AI may learn policy.
AI may learn ranking.
AI may learn veto.
AI may learn ambiguity handling.
AI may learn execution routing.
AI may learn cancel/replace behavior.
AI may learn context power.
AI may learn fractal weighting.
```

The forbidden AI role is:

```text
AI may not redefine Hook.
AI may not redefine Rally.
AI may not redefine F-counting.
AI may not redefine Node-counting.
AI may not add external indicators.
AI may not introduce non-NDS concepts.
AI may not trade directly outside gates.
```

## Short Formal Statement

NDS anatomy is a hard-rule layer. Hook, Rally, F-counting, Node-counting, and the NDS-only ontology boundary are fixed. The learnable layer begins only after NDS states are created: AI can learn how to rank, combine, veto, route, and execute NDS-native scenarios, but it cannot redefine the ontology or import external concepts.
