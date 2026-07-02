# BASE-05 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
ambiguity management principle
context power model requirement
fractal dominance requirement
origin-of-move tracking requirement
hedge/profit-protection requirement
execution gating requirement
```

## Main Design Consequence

The system needs an explicit ambiguity and context-power layer.

It is not enough to export one final state.

The system must preserve and compare:

```text
origin of move
current position inside origin-derived move
higher-scale context power
lower-scale F-count state
dominant context
competing context
execution geometry on both sides
```

## Proposed Dataset Consequences

Future datasets:

```text
ambiguity_context_ledger_v1.csv
context_power_ledger_v1.csv
origin_of_move_ledger_v1.csv
fractal_dominance_ledger_v1.csv
hedge_protection_context_v1.csv
```

## Proposed Fields

```text
move_origin_type
move_origin_f_state
move_origin_hook_state
move_origin_scale
current_position_inside_origin_move
origin_move_completion_state

higher_tf_context_power
current_tf_context_power
lower_tf_context_power

dominant_context_scale
dominant_context_direction
dominant_context_reason_vector

competing_context_alive
competing_context_reason_vector

ambiguity_score
ambiguity_class
wait_for_base_required
dual_intent_candidate
hedge_protection_candidate
```

## Proposed Classes

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

## Proposed AI Modules

```text
Ambiguity Scoring Model
Context Power Model
Origin-of-Move Analyzer
Fractal Dominance Gate
Wait-for-Base Router
Dual-Intent Detector
Hedge Protection Router
```

## Proposed Execution Policies

```text
TRADE_DOMINANT_CONTEXT
WAIT_FOR_BASE
WATCH_ONLY
NO_TRADE_AMBIGUOUS
ALLOW_DUAL_INTENT
ALLOW_HEDGE_PROTECTION
BLOCK_LOCAL_SIGNAL_BY_HIGHER_CONTEXT
```

## Open Questions

1. What exactly defines the origin of a move?
2. How far back should the system look to identify move origin?
3. Is origin determined by F3, Hook completion, node state, or a combination?
4. What makes a context powerful enough to dominate another?
5. Can a lower-timeframe F3 ever override a higher-timeframe non-terminal context?
6. When should the system wait for a Hook base before entering with the dominant higher context?
7. What is the exact difference between dual-intent and hedge protection?
8. When is hedge allowed only for profit protection, not for new risk?
9. Can both sides be traded if neither side already has profit?
10. When should higher-scale direction block lower-scale execution?
11. Should ambiguity score be feature input for every AI model?
12. Should no-trade ambiguity be a hard gate?
13. How should the system represent "wait for base" in ExecutionIntent?
14. Can context power be rule-based first before AI?
15. Which should be built first: Ambiguity Scoring Model or Context Power Model?

## Attachment Index

```text
images/BASE-05-image-01-h1-higher-timeframe-bearish-f3-energy.png
images/BASE-05-image-02-m10-lower-timeframe-bullish-f3-context.png
```
