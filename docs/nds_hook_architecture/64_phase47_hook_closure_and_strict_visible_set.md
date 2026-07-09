# Phase 47 — Hook Closure Lifecycle and Strict Valid Visible Set

## Problem

Live screenshots showed two violations:

1. **Label leakage:** when `show_only_valid_hooks` was enabled, many structural sequence labels still appeared.
2. **Terminal ambiguity:** cycle endpoints could be promoted to raw candle extremes, while the user canon defines Hook closure by a confirmed terminal node.

The result was visually misleading: a single valid family could cause an entire same-origin structural cluster to appear, making the chart look as if every Hook were valid.

## Final user canon

### Hook candidate vs closed Hook

A Hook candidate is only a candidate until its terminal node is confirmed.

For a scale `L`, confirmation means the terminal node survives its confirmation window. In the user's language:

> if the Hook has an L-node of 5, and 5 candles do not reach/violate the final node, that final node stabilizes and the Hook is closed.

### Origin death before terminal confirmation

If price touches or crosses the Hook origin before the terminal node is confirmed, the candidate was never a Hook.

It should not be labelled as failed production Hook; it should be removed from the valid Hook universe.

### Continuing before origin death

If another same-side node appears before origin death, the Hook may continue to that newer terminal node. The terminal is not frozen until the final terminal node is confirmed.

## Terminal doctrine

### Positive Hook

The terminal is:

```text
lowest confirmed valley still above origin
```

### Negative Hook

The terminal is:

```text
highest confirmed peak still below origin
```

Raw wick/candle extremes are not production Hook terminals. They may become a later diagnostic layer, but they must not own valid-only cycle endpoints.

## Strict visible-set doctrine

`show_only_valid_hooks=true` means the visible set is exact.

Allowed:

```text
F3H    Hook After Opposing F3
HH     Hook-2 After Hook-1
PARENT Hook-1 only as the explicit parent companion of a visible HH child
```

Forbidden:

```text
same-origin sibling expansion
structural fallback
unqualified sequence labels
unqualified node labels
raw Hook candidates
Phase01/Phase03-06 diagnostic overlays
```

## Implementation changes

### Visual layer

`FP_HookP02ExpandSelectionWithSameHookGroupMembers(...)` is changed to no-op.

Reason: same-origin expansion was the main source of valid-only leakage.

The only allowed expansion is:

```text
valid HH child -> its explicit parent companion
```

### Rules layer

`FP_HookP02BuildSequencesWithRates(...)` no longer promotes raw candle extremes into production terminal time/price.

Reason: raw extreme promotion conflicted with confirmed-terminal closure. The structural terminal emitted by `FP_HookP02BuildSequences(...)` remains authoritative for both visible cycle endpoint and Hook-after-Hook continuity.

## Expected result

In valid-only mode:

- fewer labels;
- no blocks of unrelated sequence numbers;
- no all-branch expansion around a valid origin;
- no raw-terminal stretched arcs;
- zero Hook drawings when no canonical valid Hook exists.
