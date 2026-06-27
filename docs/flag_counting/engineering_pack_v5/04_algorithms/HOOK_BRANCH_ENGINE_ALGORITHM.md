# Hook Branch Engine Algorithm

## Inputs

```text
PostFlagContext
NodeView(L)
direction context: bullish or bearish
adverse_side: LOW for bullish, HIGH for bearish
```

## Outputs

```text
InternalNumberingEvent
HookBranch
NDHookEvent
```

## Step 1: Collect Adverse Nodes

Bullish:

```text
adverse nodes = lows after parent Leg2 inside owned context
opposite nodes = highs between lows
```

Bearish:

```text
adverse nodes = highs after parent Leg2 inside owned context
opposite nodes = lows between highs
```

## Step 2: Build Branches From End Backward

Bullish branch rule:

```text
Starting from a later low, earlier lows that are higher can belong to the same descending branch.
A later lower low can validate/pass multiple earlier 1 candidates.
```

Bearish branch rule:

```text
Starting from a later high, earlier highs that are lower can belong to the same ascending branch.
A later higher high can validate/pass multiple earlier 1 candidates.
```

## Step 3: Chronological Labeling

After branch membership is built, reverse the branch chronologically and label:

```text
1, 2, 3, 4
```

## Step 4: Validate Minimum 1/2

A branch has valid internal 1/2 when:

Bullish:

```text
node2.low < node1.low
and there is at least one opposite high between them
```

Bearish:

```text
node2.high > node1.high
and there is at least one opposite low between them
```

## Step 5: F1 Middle Restriction

For F1 before minimum 1/2 exists:

Bullish:

```text
opposite high between 1 and 2 must not pass F1 Leg2 high
```

Bearish:

```text
opposite low between 1 and 2 must not pass F1 Leg2 low
```

After valid 1/2 exists, later 3/4 may be counted normally.

## Step 6: Branch Length Control

If any branch length > 4:

```text
increase L
recompute node view
rebuild branches
repeat until max branch length <= 4
```

Do not emit a readable hook branch with more than four numbered nodes.

## Step 7: ND Eligibility

```text
branch length == 2 => internal numbering only
branch length == 3 or 4 => ND/Hook candidate
branch length > 4 => invalid readable view, increase L
```

## Step 8: 50% Retracement

For ND candidate:

```text
cycle_size = abs(extreme.price - start.price)
retraced = abs(extreme.price - final.price)
passes = retraced > 0.50 * cycle_size
```

If input allows below-half ND, still emit but mark:

```text
half_cycle_passed = false
```

Default should not accept below-half ND.

## Step 9: Emit

Emit:

```text
InternalNumberingEvent for every valid branch
NDHookEvent for every accepted 3/4 branch
```

Each emitted event must include:

```text
hook_id
parent context id
numbered node ids
readable L
start node
extreme node
final node
half-cycle metric
```
