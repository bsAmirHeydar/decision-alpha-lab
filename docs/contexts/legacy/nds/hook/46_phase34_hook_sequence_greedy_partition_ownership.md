# Phase 34 — Hook Sequence Greedy Partition and Node Ownership

## Problem

The previous Phase 02 Hook branch engine behaved like a branch enumerator. It could emit multiple overlapping sequences from the same raw peak/valley stream. In practice, this created two errors:

1. a valid sequence could end at `2` even when valid continuation nodes existed later in the raw stream;
2. a node that already participated in one sequence could later become node `1` of another sequence.

This is not the desired Hook sequence doctrine.

## Canonical doctrine

Hook sequence construction is a partitioning problem, not a sliding-window enumeration problem.

For each scale and direction, first build the raw same-side node list in chronological order.

Positive Hook:

```text
raw_nodes = ordered valleys, old-to-new
```

Negative Hook:

```text
raw_nodes = ordered peaks, old-to-new
```

Then partition that raw list into canonical sequences.

## Positive Hook partition rule

For a positive Hook, the engine scans valleys old-to-new:

```text
1. Take the first unused valley.
2. Assign it as node 1 of the current sequence.
3. Continue scanning to the end of the raw valley list.
4. Every unused valley that is strictly lower than the last accepted valley is appended as the next sequence node.
5. When the scan reaches the end of the list, the sequence is complete.
6. All nodes that participated in the sequence are marked consumed.
7. The next sequence starts from the next unused raw valley.
8. Repeat until the raw list is exhausted.
```

Example:

```text
Raw valleys:
A=100, B=98, C=101, D=97, E=99, F=96

Sequence 1:
A(1) -> B(2) -> D(3) -> F(4)

Consumed:
A, B, D, F

Sequence 2:
C(1) -> E(2)
```

The first sequence is not allowed to stop at `B(2)` if `D(3)` and `F(4)` exist later in the list.

`B`, `D`, or `F` are not allowed to become node `1` of another overlapping sequence.

## Negative Hook partition rule

For a negative Hook, the same rule applies to ordered peaks:

```text
1. Take the first unused peak.
2. Assign it as node 1.
3. Continue scanning to the end of the raw peak list.
4. Every unused peak that is strictly higher than the last accepted peak is appended.
5. Mark all participating peaks consumed.
6. Start the next sequence from the next unused peak.
```

## Node ownership rule

A raw same-side node may belong to one canonical Phase 02 sequence only.

```text
consumed node = cannot seed a later sequence
consumed node = cannot be reused inside another overlapping sequence
```

This differs from the earlier exploratory branch view, where the same physical chart node could appear in several branches with different numbers. That behavior is now treated as a debug-only enumeration style and is not valid for production Hook counting.

## Hook-after-Hook exception

The only allowed structural sharing is at the Hook-object level:

```text
previous Hook terminal = next Hook origin
```

That shared node may become the origin/start of the next Hook object, but it must not become node `1` of the next internal sequence.

## Implementation change

`FP_HookPhase02Rules.mqh` now builds sequences through a canonical greedy partition:

```text
for each scale and direction:
    collect same-side nodes old-to-new
    consumed[] = false
    for each node in raw list:
        if consumed: skip
        start new sequence at this node as 1
        scan forward to end
        append stricter unused nodes
        mark appended nodes consumed
```

Positive continuation:

```text
candidate_valley < previous_accepted_valley
```

Negative continuation:

```text
candidate_peak > previous_accepted_peak
```

## Display capacity

The Phase 02 visual structure stores labels `1..4`. If a greedy sequence continues beyond four nodes, the full terminal/resolve node remains the actual last accepted node, while the readable chart labels show the first four slots and the sequence is marked capped.

This prevents the old failure mode where a long valid sequence was rejected and its later nodes were then reused as misleading new sequence starters.

## Expected chart behavior

After this patch:

- repeated `B1:1`, `B2:1`, `B3:1` labels from overlapping reuse should be reduced;
- a sequence should continue to `3` and `4` when later valid continuation nodes exist;
- already-consumed raw valleys/peaks should not restart new sequence numbering;
- the Hook view should become less fractal, less noisy, and closer to the intended canonical sequence structure.
