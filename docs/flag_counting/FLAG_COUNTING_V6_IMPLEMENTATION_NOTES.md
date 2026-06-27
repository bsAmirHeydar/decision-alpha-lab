# Flag Counting V6 Implementation Notes

This patch adds a new implementation namespace: `FlagCountingV6`.

V6 is not a patch over the old scanner. It is a modular implementation intended to follow the engineering documentation pack:

1. L-rule node extraction from candle highs/lows.
2. Equal high/low plateau merge.
3. Alternating node view per L.
4. Two-leg flag body construction.
5. F1/F2/F3 post-flag state evaluation.
6. Backfilled F2/F3 child origins from the parent post-flag correction context.
7. Branch-based ND/Hook extraction.
8. Diagnostic renderer that only draws emitted logical objects.

## Compile target

```text
mql5/Experts/FlagCounting/FlagCountingV6Experiment.mq5
```

## Important implementation choices

### Node definition

The node engine follows the project L-rule:

- High/low only.
- Equal price is not a break.
- A node becomes confirmed when at least `L` candles on the right side do not reach beyond that price.
- Equal highs/lows are merged into a plateau node.
- The plateau stores a time interval and uses the latest equal touch as the drawing anchor.

### Flag body

A flag body is always:

```text
Origin -> Leg1 -> Waist -> Leg2
```

The body is the same for F1/F2/F3. The difference is only post-body behavior.

### F1

F1 is drawn after a two-leg body is complete.

F1 confirmation requires:

1. A post-flag internal `1/2` or more.
2. For the minimum `1/2`, the middle node between `1` and `2` must not break the F1 flag endpoint.
3. Then the F1 Leg2 endpoint must be strictly broken.

F1 invalidation before confirmation is the F1 waist.

### F2

F2 is authorized only after F1 confirmation, but its origin is backfilled from the deepest adverse correction after the F1 flag.

F2 must satisfy size relative to F1:

```text
F2.flag_size >= F1.flag_size * InpF2MinParentSizeRatio
```

F2 is not rejected while waiting for size. It can continue via Leg2 extension.

F2 invalidation is its own origin. If it dies, the parent F1 context remains alive.

### F3

F3 is authorized only after F2 confirmation, but its origin is backfilled from the deepest adverse correction after the F2 flag.

F3 completion uses an OR rule:

```text
F3.leg1_L >= ceil(0.80 * F2.leg1_L)
OR
F3.flag_size > 0.70 * F2.flag_size
```

F3 is not rejected while waiting for the OR rule. It can continue via Leg2 extension.

F3 locks when the first confirmed opposite F1 appears after F3 completion.

### ND / Hook

The ND/Hook engine is branch-based. It does not blindly label every sliding window.

ND is emitted when a hook branch has 3 or 4 adverse-side readable nodes. Two nodes are not ND.

The 50% rule is implemented as retracement from branch extreme toward branch start.

### Renderer

Renderer rules:

- Thin fixed line width by default.
- F body: straight line for `Origin -> Leg1`, smooth segmented curve for `Leg1 -> Waist -> Leg2`.
- ND/Hook: gray arc.
- Detailed labels by default: `F1 L8 Q23 status`.
- Origin label `O` shown by default.
- Internal numbers shown by default.
- Renderer does not create logical structures.

## Compile caveat

This patch was generated outside MetaEditor. The zip was built and tested, but a real MetaEditor compile must still be run locally. If MetaEditor reports a compile error, fix only the specific file and line; do not rewrite the logic again.

## V6.1 semantic visibility and ownership repair

The screenshot audit after the first V6 pass showed that the engine was drawing a
raw audit dump instead of a semantic chart view.  V6.1 therefore separates three
concerns more strictly:

1. **Logic state**: sequence events emitted by the engine.
2. **Audit state**: raw seeds, intermediate transitions, and full verbose logs.
3. **Main chart state**: only the semantically useful current state of each chain.

### Main chart is no longer an audit dump

The renderer now has explicit controls for:

```text
InpDrawRawSeeds = false
InpDrawLifecycleHistory = false
InpShowParentIds = true
InpLabelTimeClusterBars = 4
InpLabelPriceClusterPoints = 160
```

With these defaults, raw seed attempts stay out of the main chart.  If a sequence
has progressed from `post_flag` to `confirmed` or from `completed` to `locked`,
the older lifecycle state is suppressed in the main chart unless
`InpDrawLifecycleHistory=true` is enabled.

### F1 phase-boundary gate

Root F1 creation is now gated by phase boundaries.  The engine no longer treats
every arbitrary two-leg window as a root F1 by default.  A root F1 must be anchored
to a readable ND/Hook boundary for the same direction when such a boundary exists
for the scale.  The input is:

```text
InpRequireF1PhaseBoundary = true
```

The gate is fail-open only when no readable ND/Hook boundary exists for that
scale/direction.  This avoids empty charts while still preventing the worst
mid-move sliding-window F1 starts.

### Backfill context is bounded by parent confirmation

F2/F3 backfill must come from the actual post-flag correction that confirmed the
parent, not from any future correction on the chart.  V6.1 changes the deepest
adverse correction search to:

```text
F2 origin search: after F1 Leg2 and before F1 confirmation
F3 origin search: after F2 Leg2 and before F2 confirmation
```

This fixes a major ownership bug where child origins could be pulled from a much
later move and then drawn as if they belonged to the parent chain.

### F3 locking is future-context only

An F3 can only be locked by an opposite confirmed F1 whose origin and confirmation
occur after the F3 completion node.  Historical opposite F1s no longer lock later
F3 candidates.

### Lifecycle suppression is renderer-side only

The engine still keeps events available for verbose audit.  The renderer suppresses
superseded lifecycle states by default so the main chart shows the current logical
state rather than every transition label.

## V6 Semantic Repair: main-view ownership and restart gating

The main chart must never become a raw lifecycle dump.  The detector may still
create audit-level attempts, transitions, and candidates, but the default render
view should only expose semantically meaningful structures.  The repair layer
adds the following constraints:

1. **Root F1 phase-boundary origin selection**
   - When readable ND/Hook boundaries exist, F1 roots are built only from the
     hook adverse extreme for that direction.
   - Bullish F1 roots therefore come from the lowest LOW of the positive hook.
   - Bearish F1 roots come from the highest HIGH of the negative hook.
   - The old fail-open all-origin scan remains only for cases where no readable
     hook boundary exists at all, so the chart does not become empty while a
     phase is still developing.

2. **Single active same-direction chain per scale until opposite F3**
   - Within the same L scale and direction, a new independent F1 root is not
     allowed to start merely because another two-leg body appears.
   - A same-direction restart becomes visible only after an opposite F3 has
     completed or locked between the previous same-direction root and the new
     root.
   - This implements the contract that a direction does not keep restarting F1
     while the higher sequence is still working.

3. **Parent id rebuild after sorting and pruning**
   - Event ids are display/audit ids and can change after chronological sorting.
   - Parent ids are rebuilt after semantic pruning so labels such as `P123`
     point to the visible parent event id rather than a stale insertion id.

4. **Visual duplicate suppression**
   - Exact same body geometry with the same level, direction, and status is
     rendered once in the default view.
   - This prevents stacked duplicate labels when multiple scales converge to the
     exact same Origin/Leg1/Waist/Leg2 identity.
   - The underlying audit can still retain the separate scale discoveries.

5. **Cluster label spacing**
   - Label lanes now use stronger vertical spacing so large label clusters remain
     readable when many valid events occur in the same price/time area.

These rules are deliberately applied after all scales are scanned.  F3 locks and
same-direction restart pruning need a cross-scale, full-history view of the
current run.  The renderer still remains non-authoritative: it only hides or
merges display duplicates; it does not invent or mutate logical structures.
