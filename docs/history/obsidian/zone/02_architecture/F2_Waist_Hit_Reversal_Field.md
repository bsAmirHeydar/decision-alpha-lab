---
type: architecture_note
status: canonical
language: english
project: Decision Alpha Lab
related:
  - F2_Waist_Hit_Point1_Point2
  - F2_Zone
  - Parent_Child_Zone
---

# F2 Waist-Hit Reversal Field

The F2 waist-hit reversal field is created when the waist contact re-anchors the F2 grammar.

```text
waist contact → Point 1
next hit/extension → Point 2
from Point 2 onward/beyond → reversal field
```

The field is not automatically an execution zone. It is a parent context that says: reversal can begin from here, but execution requires a smaller risk contract.

## Architecture

```text
F2 Parent Context
  ↓
Waist-Hit Re-Anchor
  ↓
Point 1 at Waist
  ↓
Point 2 after Extension/Hit
  ↓
Active Reversal Field
  ↓
Lower-Timeframe Child Zone Search
  ↓
Limit Entry if Child Stop Is Stable
```

## Failure Mode

The main failure is treating the parent reversal field as a complete trade.

That violates the Alpha Lab doctrine:

```text
Potential area is not enough.
A tradable zone needs a start and a stop.
```
