# BASE-01 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
core ontology principle
feature family
AI architecture requirement
execution safety requirement
```

It is not a simple trading rule. It defines how the whole system should represent market state.

## Key Open Questions

1. What exactly makes a Hook alive?
2. What exactly makes a Hook closed?
3. What exactly makes a Rally valid?
4. When does Rally F-counting start?
5. When is a Rally later reclassified as Hook-building?
6. Which scale has authority when parent and current interpretations conflict?
7. Should all four direction/context hypotheses always be exported, or only the alive ones?
8. Should the system assign scores to each hypothesis or only classify them as alive/dead?
9. What does it mean for one hypothesis to dominate another?
10. When ambiguity is high, should the execution router watch, delay, or block?

## Proposed Dataset Path

The first dataset affected by this experience:

```text
canonical_state_packet_v1.csv
```

Future specialized dataset:

```text
multi_hypothesis_context_ledger_v1.csv
```

## Proposed Fields

```text
bullish_hook_alive
bullish_hook_quality
bullish_rally_alive
bullish_rally_quality
bearish_hook_alive
bearish_hook_quality
bearish_rally_alive
bearish_rally_quality
dominant_direction_hypothesis
dominant_context_hypothesis
ambiguity_score
parent_current_alignment
current_child_alignment
fractal_context_state
```

## Proposed AI Modules

```text
Dual Direction Ranker
Hook/Rally Ambiguity Model
Fractal Context Model
Ambiguity Gate
Execution Router
```

## Attachment Index

```text
BASE-01-image-01-bearish-rally-inside-hook.png
BASE-01-image-02-bullish-rally-inside-larger-hook.png
```
