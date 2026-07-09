# 57 — Hook Sequence, Terminal, and Cycle Policy

## Status

Canonical doctrine.  
This document defines the structural counting and cycle-terminal semantics used before valid-only rendering.

## Key separation

Hook counting and Hook validity are different layers.

```text
Hook counting = structural completeness
Hook validity = production visibility filter
```

The sequence builder must not become too restrictive because of production-view needs.

---

# 1. Raw material for Hook sequences

## 1.1 Positive Hook

A positive Hook is built from valleys ordered from old to new.

```text
positive_hook_raw_nodes = valleys(old -> new)
```

## 1.2 Negative Hook

A negative Hook is built from peaks ordered from old to new.

```text
negative_hook_raw_nodes = peaks(old -> new)
```

## 1.3 Node source

The raw material should come from the project’s canonical Hook/Phase01 swing-node stream unless a separate document explicitly replaces that source.

The terminal for drawing may use raw candle extremes, but the sequence itself is still built from structural nodes.

---

# 2. Sequence construction

## 2.1 Seed selection

The builder scans the raw node list from old to new.

The first node that has not previously participated in earlier sequences as a member becomes node `1` of the next sequence.

```text
first unused raw node => sequence node 1
```

## 2.2 Positive continuation

For a positive Hook sequence:

```text
node 1 = first unused valley
node 2 = next valley lower than node 1
node 3 = next valley lower than node 2
node 4 = next valley lower than node 3
...
```

The scan continues forward through the entire raw list.

A higher valley does not terminate the scan. It is skipped. If a later lower valley appears, it becomes the next sequence node.

Example:

```text
Valleys: A=100, B=98, C=101, D=97, E=99, F=96
Sequence 1: A:1 -> B:2 -> D:3 -> F:4
Sequence 2: C:1 -> E:2
```

## 2.3 Negative continuation

For a negative Hook sequence:

```text
node 1 = first unused peak
node 2 = next peak higher than node 1
node 3 = next peak higher than node 2
node 4 = next peak higher than node 3
...
```

The scan continues forward through the entire raw list.

A lower peak does not terminate the scan. It is skipped. If a later higher peak appears, it becomes the next sequence node.

---

# 3. Participation rule

## 3.1 Cannot restart as node 1

A node that has participated in a previous sequence cannot become node `1` of a later sequence.

```text
participated_before(node) => cannot_seed_new_sequence_as_1
```

## 3.2 Continuation reuse

A participated node may still appear as node `2`, `3`, `4`, etc. of a later sequence if the forward scan naturally reaches it and the strict continuation rule requires it.

```text
participated_before(node) does not imply forbidden_as_continuation
```

This distinction is important. Over-restricting reuse causes too few Hooks. Allowing used nodes to restart as node 1 causes noisy overcounting.

Correct doctrine:

```text
Used node cannot restart.
Used node may continue.
```

---

# 4. Sequence length and labels

The internal sequence may continue beyond four nodes.

For chart readability, production labels may display only the first four sequence numbers:

```text
B1:1
B1:2
B1:3
B1:4
```

However, the true terminal of the sequence/cycle must still use the actual deepest/highest valid endpoint, not merely the fourth displayed label.

---

# 5. Positive Hook terminal

## 5.1 Structural definition

For a positive Hook, the terminal is the lowest valley reached that remains above the Hook origin/start boundary.

```text
positive_hook_terminal = lowest valley above origin
```

This is not simply the last displayed sequence label.

## 5.2 Raw drawing endpoint

For the cycle arc, the drawing endpoint may use the raw price/time of the lowest observed low associated with that terminal area, provided it remains above the Hook origin boundary.

```text
cycle_end_price = lowest observed terminal-side low above origin
cycle_end_time  = time of that low
```

If the price breaches the origin before terminal confirmation, the candidate is not a valid Hook candidate.

---

# 6. Negative Hook terminal

The negative Hook terminal is the mirror definition:

```text
negative_hook_terminal = highest peak below origin
```

For the cycle arc:

```text
cycle_end_price = highest observed terminal-side high below origin
cycle_end_time  = time of that high
```

---

# 7. Cycle arc geometry

A Hook cycle arc has three conceptual anchors:

```text
Arc start = Hook origin
Arc crown = opposite extreme / crown
Arc end = terminal extreme
```

For positive Hook:

```text
origin = start valley / death boundary
crown  = opposite peak
end    = lowest terminal valley/low above origin
```

For negative Hook:

```text
origin = start peak / death boundary
crown  = opposite valley
end    = highest terminal peak/high below origin
```

---

# 8. Origin breach lifecycle

If the Hook origin is breached before the terminal is confirmed:

```text
candidate = non-hook
```

It should not be rendered in production view.

If the Hook terminal/cycle has already been confirmed, a later origin breach is a failure/invalidation event, not proof that the Hook never existed. This behavior is for later failure/zone logic and is out of scope for this document.

---

# 9. Implementation contract

The implementation must expose both:

1. **Structural terminal node** — for Hook-after-Hook continuity and sequence ownership.
2. **Cycle drawing terminal price/time** — for rendering the arc to the true observed terminal extreme.

Do not collapse these two fields into one ambiguous endpoint.
