<!-- CURRENT CANON NOTICE
This file is retained as historical/context documentation. For current Phoenix implementation decisions, use:

docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting Sequence Contract V3

Status: implementation contract, English canonical version.

This document replaces the previous loose flag-counting descriptions. It defines the deterministic sequence logic for `F1 -> F2 -> F3`, ND/Hook detection, adaptive node compression, invalidation, confirmation, rendering identity, and the remaining implementation knobs.

The goal is not to scan arbitrary four-node windows and draw them. The goal is to preserve every raw high/low observation, build scale-aware views from those observations, and assign every meaningful movement to a coherent structural state without creating orphan flags from the middle of a move.

---

## 1. Core Philosophy

### 1.1 The engine is high/low based

The entire Flag Counting model works on swing high and swing low geometry.

The following values are not part of F or ND definitions:

- candle open
- candle close
- candle body
- candle color
- whether a candle closed beyond a level

This does not mean that candle close is forbidden. It means candle close is irrelevant. If a node happens to coincide with a candle close, nothing special happens. The detector only sees the swing high / swing low node geometry.

Canonical statement:

```text
Flag Counting is high/low-node based and open/close agnostic.
```

### 1.2 All raw highs and lows are preserved

The system must never destroy raw high/low observations. Raw nodes are the source of truth.

However, the engine is allowed to read those raw nodes through different scale lenses. In many contexts, the system must merge smaller alternating nodes into a larger-scale view by increasing the compression level `L` until the current structure becomes readable.

This means:

```text
Raw data is preserved.
Structural interpretation is scale-compressed.
```

### 1.3 A flag is always a two-leg body

A flag body is always the same kind of object:

```text
Origin -> Leg1 -> Waist -> Leg2
```

The difference between F1, F2, and F3 is not the two-leg body itself. The difference is what must happen after that two-leg body.

- F1 requires post-flag internal `1/2` or more before it can confirm.
- F2 requires post-flag internal `1/2` or more before it can confirm, but its post-flag correction is allowed to break the flag waist as long as it does not break the origin/start of Leg1.
- F3 is completed by its two-leg body. After F3 completes, the chain is terminal. The remaining same-direction movement is treated as F3 extension until the first smallest confirmed opposite F1 appears.

### 1.4 The sequence is ordered

Within a sequence and scale context, flags are ordered:

```text
F1 -> F2 -> F3
```

After F1 confirms, the engine must seek F2, not another F1 inside the same chain.

After F2 confirms, the engine must seek F3, not another F1 or F2 inside the same chain.

This rule is critical. The detector must not restart from F1 every time a new local four-node body appears.

### 1.5 No idle movement

A major design requirement is that movement must not be structurally idle.

F1 must not start from a random point in the middle of an already active move. An F1 start must be explainable as one of the following:

1. after an ND/Hook phase,
2. after the terminal endpoint of an opposite flag sequence,
3. after the smallest confirmed opposite F1 that locks a prior F3 extension.

This rule exists to prevent the chart from being filled with orphan lines that have no structural parent or phase origin.

---

## 2. Node Model

### 2.1 Raw node

A raw node is a swing observation:

```text
node_id
bar_time
bar_index
price
kind = HIGH or LOW
source_L = 2 by default for base scanning
```

The base source node level starts at `L = 2`. Raw nodes must remain available even if larger-scale views are created.

### 2.2 Scaled node view

A scaled node view is not a new market reality. It is a compressed reading of raw high/low nodes.

The scaled view must be alternating:

```text
HIGH -> LOW -> HIGH -> LOW
```

or:

```text
LOW -> HIGH -> LOW -> HIGH
```

If multiple consecutive nodes of the same type appear inside a scale view, they must be merged by keeping the extreme relevant node:

- consecutive HIGH nodes: keep the highest high,
- consecutive LOW nodes: keep the lowest low.

The discarded smaller nodes are not deleted from raw storage. They are only hidden from this specific scaled interpretation.

### 2.3 Adaptive compression

When a structure has too many readable nodes, the engine increases `L` until the structure has four or fewer nodes.

Canonical rule:

```text
If readable node count > 4:
    increase L
    rebuild compressed alternating view
    repeat until node count <= 4
```

For ND/Hook specifically:

- 3 nodes = ND/Hook candidate,
- 4 nodes = ND/Hook candidate,
- 2 nodes = not ND,
- more than 4 nodes = increase `L` until `<= 4`.

### 2.4 The start node of an ND cycle

For ND/Hook detection, the cycle start node is anchored from the base node stream. The start anchor should not be moved simply because downstream compression changes.

Practical implementation:

```text
ND start anchor: base L=2 node
Downstream nodes: may be compressed by increasing L
Goal: reduce the cycle view to 4 or fewer nodes without moving the conceptual start anchor
```

This keeps ND identity stable while still allowing the middle of the cycle to be read at a larger scale.

---

## 3. Flag Body Geometry

### 3.1 Bullish flag body

A bullish flag body has this shape:

```text
Origin = LOW
Leg1   = highest HIGH before the correction
Waist  = deepest LOW of the correction after Leg1 and before Leg2
Leg2   = HIGH that breaks Leg1
```

The body size is:

```text
flag_size = abs(Leg2.price - Origin.price)
```

The correction after Leg1 must not break the Origin. If it breaks the Origin, this body is not a valid flag body.

Important: Leg1 is not necessarily the first high after the Origin. Leg1 is the final/highest high before the meaningful correction that creates the Waist.

### 3.2 Bearish flag body

A bearish flag body is the inverse:

```text
Origin = HIGH
Leg1   = lowest LOW before the correction
Waist  = highest HIGH of the correction after Leg1 and before Leg2
Leg2   = LOW that breaks Leg1
```

The body size is:

```text
flag_size = abs(Leg2.price - Origin.price)
```

The correction after Leg1 must not break the Origin. If it breaks the Origin, this body is not a valid flag body.

### 3.3 Waist update rule

The Waist is dynamic until Leg2 is established.

Bullish case:

```text
After Leg1, keep updating Waist to the deepest correction LOW
until Leg1 is broken upward into Leg2.
```

Bearish case:

```text
After Leg1, keep updating Waist to the highest correction HIGH
until Leg1 is broken downward into Leg2.
```

This prevents the renderer and detector from using the first correction node as the waist when a deeper correction appears before the actual continuation.

### 3.4 Leg2 extension before post-flag correction qualifies

After the two-leg body is hit, if the market does not create valid post-flag internal `1/2` or more and instead continues beyond the current Leg2 endpoint, the old Leg2 endpoint must be discarded as a final endpoint.

The movement still belongs to the same flag body.

Bullish case:

```text
If after Leg2 the market does not produce valid internal 1/2,
and then makes a higher high beyond Leg2,
then update Leg2 to the higher high.
```

Bearish case:

```text
If after Leg2 the market does not produce valid internal 1/2,
and then makes a lower low beyond Leg2,
then update Leg2 to the lower low.
```

This is especially important in F1, but the same principle applies to F2 and the pre-terminal part of F3.

---

## 4. Internal Post-Flag Numbering

### 4.1 Internal numbers are created after the flag body

Internal `1`, `2`, `3`, and `4` are not inside the two-leg body. They are built in the correction after Leg2.

The two-leg flag body is:

```text
Origin -> Leg1 -> Waist -> Leg2
```

The post-flag correction is what can produce:

```text
1 / 2
```

or:

```text
1 / 2 / 3
```

or:

```text
1 / 2 / 3 / 4
```

### 4.2 Bullish internal 1/2

After a bullish flag body completes at a high Leg2, the internal correction is bearish/pullback geometry.

For a valid bullish post-flag `1/2` structure:

```text
1 = first meaningful LOW after Leg2
middle opposite node = HIGH between 1 and 2
2 = later LOW below 1
```

So the shape is:

```text
LOW(1) -> HIGH(middle) -> LOW(2)
```

The key condition:

```text
2 must be below 1.
```

For F1 specifically, the middle HIGH between 1 and 2 must not break above the F1 Leg2 endpoint.

For F2, the middle HIGH between 1 and 2 is allowed to break above the F2 Leg2 endpoint.

For F3, post-flag correction is not required for completion.

### 4.3 Bearish internal 1/2

After a bearish flag body completes at a low Leg2, the internal correction is bullish/pullback geometry.

For a valid bearish post-flag `1/2` structure:

```text
1 = first meaningful HIGH after Leg2
middle opposite node = LOW between 1 and 2
2 = later HIGH above 1
```

So the shape is:

```text
HIGH(1) -> LOW(middle) -> HIGH(2)
```

The key condition:

```text
2 must be above 1.
```

For F1 specifically, the middle LOW between 1 and 2 must not break below the F1 Leg2 endpoint.

For F2, the middle LOW between 1 and 2 is allowed to break below the F2 Leg2 endpoint.

For F3, post-flag correction is not required for completion.

### 4.4 More than two internal numbers

If the post-flag correction creates 3 or 4 readable nodes, the system must label them numerically:

```text
1 / 2 / 3
```

or:

```text
1 / 2 / 3 / 4
```

If the compressed post-flag correction has exactly 3 or 4 nodes, it is also an ND/Hook zone and must get an `ND` label at the end of that correction.

If the compressed post-flag correction has exactly 2 nodes, it is internal structure but not ND.

If it has more than 4 nodes, increase `L` until it becomes 4 or fewer nodes.

---

## 5. F1 Contract

### 5.1 F1 start rule

F1 can start only from a meaningful phase boundary:

1. after ND/Hook,
2. after an opposite flag sequence endpoint,
3. after a previous F3 has been locked by the first smallest confirmed opposite F1.

F1 must not be created from the middle of an already active unassigned move.

### 5.2 F1 body

F1 body is a normal two-leg flag body:

```text
Origin -> Leg1 -> Waist -> Leg2
```

Bullish F1:

```text
Origin = LOW
Leg1 = highest HIGH before correction
Waist = deepest LOW after Leg1 before Leg2
Leg2 = HIGH breaking Leg1
```

Bearish F1:

```text
Origin = HIGH
Leg1 = lowest LOW before correction
Waist = highest HIGH after Leg1 before Leg2
Leg2 = LOW breaking Leg1
```

### 5.3 F1 invalidation

For F1, the post-flag invalidation boundary is the flag Waist.

Bullish F1:

```text
If post-flag correction hits/breaks below the F1 Waist before F1 confirms,
F1 invalidates.
```

Bearish F1:

```text
If post-flag correction hits/breaks above the F1 Waist before F1 confirms,
F1 invalidates.
```

If the body correction after Leg1 breaks the Origin before Leg2 exists, the candidate flag body is invalid and must be removed.

### 5.4 F1 confirmation

F1 confirms when all of the following happen:

1. the two-leg flag body exists,
2. post-flag internal `1/2` or more appears before the F1 Waist is hit,
3. price then breaks the F1 flag endpoint / Leg2 extreme again using high/low geometry.

Bullish F1 confirmation:

```text
After internal 1/2 or more,
if a HIGH breaks above F1 Leg2,
F1 is confirmed.
```

Bearish F1 confirmation:

```text
After internal 1/2 or more,
if a LOW breaks below F1 Leg2,
F1 is confirmed.
```

### 5.5 F1 extension when no internal 1/2 appears

If F1 has completed the two-leg body but does not produce internal `1/2` or more and instead breaks beyond Leg2, that move is still part of F1 Leg2.

The old Leg2 endpoint is replaced.

The flag is not considered confirmed until internal `1/2` or more appears and then Leg2 is broken again.

---

## 6. F2 Contract

### 6.1 F2 is built only after F1 confirmation

F2 must not be built before F1 confirms.

Candidate F2 may be tracked internally only after F1 confirmation. The displayed F2 should come from the post-F1 correction context.

### 6.2 F2 origin

F2 starts from the farthest/deepest terminal correction node after the F1 flag body correction.

Bullish chain:

```text
F2 Origin = deepest LOW in the post-F1 correction context,
after adaptive compression and internal numbering.
```

Bearish chain:

```text
F2 Origin = highest HIGH in the post-F1 correction context,
after adaptive compression and internal numbering.
```

If post-F1 correction has more than two internal numbers, the origin is not arbitrarily the first `2`. It is the terminal/deepest correction extreme that represents the actual end of the post-F1 correction context.

### 6.3 F2 body

F2 body is also:

```text
Origin -> Leg1 -> Waist -> Leg2
```

F2 body size is:

```text
F2_flag_size = abs(F2.Leg2.price - F2.Origin.price)
```

F2 should respect the size relationship already established in prior discussions:

```text
F2_flag_size >= F1_flag_size
```

This size rule may be configurable, but the default contract is `>=`.

### 6.4 F2 invalidation

F2 differs from F1 after its flag body.

For F2, hitting the Waist after the flag body does not necessarily invalidate the structure.

F2 invalidation boundary is the start of Leg1, i.e. the Origin of the F2 body.

Bullish F2:

```text
If post-flag movement hits/breaks below F2 Origin,
then this was not a valid F2.
```

Bearish F2:

```text
If post-flag movement hits/breaks above F2 Origin,
then this was not a valid F2.
```

When an F2 candidate dies this way, F1 remains alive if F1 itself has not invalidated. The engine continues seeking F2 from the same post-F1 correction context.

### 6.5 F2 waist-break branch

If F2 post-flag movement breaks the F2 Waist but does not break the F2 Origin, F2 does not die.

Instead, this becomes a valid waist-break branch:

```text
1 = F2 Waist
2 = node that breaks the F2 Waist
```

Then F2 confirms only if price later breaks the F2 flag endpoint / Leg2 extreme.

Bullish F2:

```text
If after the waist-break branch a HIGH breaks above F2 Leg2,
F2 is confirmed.
```

Bearish F2:

```text
If after the waist-break branch a LOW breaks below F2 Leg2,
F2 is confirmed.
```

### 6.6 F2 confirmation

F2 confirms when:

1. F2 body exists,
2. post-flag internal `1/2` or more exists, or valid waist-break branch exists,
3. price breaks the F2 Leg2 endpoint again.

---

## 7. F3 Contract

### 7.1 F3 is built after F2 confirmation

F3 is sought only after F2 has confirmed.

The chain is:

```text
F1 confirmed -> seek F2
F2 confirmed -> seek F3
F3 completed -> terminal extension / lock process
```

### 7.2 F3 origin

F3 starts from the correction after the F2 flag.

Bullish chain:

```text
F3 Origin = relevant LOW correction after F2 flag context.
```

Bearish chain:

```text
F3 Origin = relevant HIGH correction after F2 flag context.
```

### 7.3 F3 completion

F3 does not require post-flag internal `1/2` to be complete.

F3 is completed by its two-leg flag body.

```text
F3 complete = Origin -> Leg1 -> Waist -> Leg2 exists
```

However, F3 must be same-scale compatible with F2 using the rules below.

### 7.4 F3 same-scale compatibility

F3 same-scale compatibility is checked after F3 fully breaks the F2 direction and its start is the correction after the F2 flag.

The check is evaluated for F3 Leg2 qualification.

The conditions are OR conditions, not AND conditions. F3 is accepted if either one is true.

#### Condition 1: F3 Leg1 scale compatibility

Let:

```text
F2_leg1_L = L value associated with the end of F2 Leg1
F3_leg1_L = L value associated with the end of F3 Leg1
```

Then F3 passes Condition 1 if:

```text
F3_leg1_L >= 0.80 * F2_leg1_L
```

In integer implementation, use:

```text
F3_leg1_L >= ceil(0.80 * F2_leg1_L)
```

This means F3 Leg1 may be within 20% below F2 Leg1 scale or larger.

#### Condition 2: F3 flag-size compatibility

Let:

```text
F2_flag_size = abs(F2.Leg2.price - F2.Origin.price)
F3_flag_size = abs(F3.Leg2.price - F3.Origin.price)
```

Then F3 passes Condition 2 if:

```text
F3_flag_size >= 0.70 * F2_flag_size
```

F3 is valid if either Condition 1 or Condition 2 is true.

### 7.5 F3 extension

Once F3 completes, the rest of the same-direction move is treated as F3 extension.

No F4 is created.

If the market keeps moving in the F3 direction, the F3 extension grows.

### 7.6 F3 lock

F3 locks when the first smallest confirmed opposite F1 appears.

The word `smallest` means the smallest available confirmed opposite F1, not a raw live seed.

F3 must not lock on an unconfirmed opposite candidate because that would prematurely terminate a valid F3 extension.

Once F3 locks:

- the sequence is finished,
- the F3 structure is not deleted from the chart,
- even if the entire move reverses, the locked F3 remains as historical completed structure,
- new sequence logic can begin after the opposite confirmed F1 context.

---

## 8. ND / Hook Contract

### 8.1 ND is a phase, not a flag

ND/Hook is a non-flag phase or hook structure. It can exist:

- before F1,
- after a flag body,
- inside a larger structure,
- overlapping a visible F structure.

ND is text-only in default rendering. It should not add extra body lines unless debug mode explicitly asks for it.

### 8.2 ND node count

ND requires exactly 3 or 4 compressed readable nodes.

```text
compressed_count == 3 -> ND candidate
compressed_count == 4 -> ND candidate
compressed_count == 2 -> not ND
compressed_count > 4 -> increase L until <= 4
```

If the result is still not 3 or 4 after valid compression, no ND label is created.

### 8.3 ND cycle retracement rule

ND requires that the final node has retraced more than 50% of the cycle.

Define:

```text
start_price = price of the first node of the ND cycle
extreme_price = farthest price reached from start during the cycle
last_price = price of the final compressed node
cycle_range = abs(extreme_price - start_price)
retraced_distance = abs(extreme_price - last_price)
retracement_ratio = retraced_distance / cycle_range
```

Default ND threshold:

```text
retracement_ratio >= 0.50
```

This means the last node must have come back more than half of the distance from the cycle extreme toward the start.

This is not based on candle close. It is based on high/low node prices only.

### 8.4 Optional below-50 mode

The engine should expose an input that can allow sub-50 ND candidates later.

Default:

```text
InpNDAllowBelowHalfCycle = false
InpNDMinRetracementRatio = 0.50
```

Optional research mode:

```text
InpNDAllowBelowHalfCycle = true
```

When enabled, the detector may keep ND candidates below 50%, but they should be marked differently in audit data and possibly lighter in rendering.

### 8.5 ND numbering

If a post-flag correction has 3 or 4 compressed nodes, the detector must:

1. label the internal numbers `1/2/3` or `1/2/3/4`,
2. add an `ND` label at the terminal/end area of that correction.

Two-node corrections get internal numbering but do not get ND.

### 8.6 ND overlap with F

ND can overlap F structures.

If an ND and an F occupy the same area, both can be displayed:

- F draws body and labels,
- ND draws text-only label,
- layout engine stacks labels cleanly.

---

## 9. Sequence Lifecycle

### 9.1 Main sequence states

A sequence can be represented as:

```text
WAITING_FOR_F1
F1_BODY_LIVE
F1_POST_FLAG_CORRECTION
F1_CONFIRMED
SEEKING_F2
F2_BODY_LIVE
F2_POST_FLAG_CORRECTION
F2_CONFIRMED
SEEKING_F3
F3_BODY_LIVE
F3_COMPLETED_EXTENDING
F3_LOCKED
SEQUENCE_DONE
```

Invalidated candidates are not main display states. They are audit outcomes.

### 9.2 Candidate visibility

Candidates should become visible when a probable flag body has been hit.

Raw seeds should not be drawn.

Canonical rendering status:

```text
RAW_SEED: hidden
LIVE_BODY / CANDIDATE_FLAG: visible with candidate color
POST_FLAG_CORRECTION: visible with candidate/live color and internal numbers
CONFIRMED: visible with confirmed color
LOCKED: visible as completed historical structure
INVALIDATED / REJECTED: hidden from main chart, audit only
```

This keeps all important live structures visible without returning to the old problem of drawing every raw four-node window.

### 9.3 F2 failure does not kill F1

If an F2 candidate hits its own Origin/start of Leg1, then that F2 was not F2.

The parent F1 remains alive if F1 itself remains valid.

The engine continues seeking F2 from the same F1 post-flag correction context.

Important:

```text
Do not abandon F2 search while F1 is alive.
Do not reuse a dead F2 origin as if it were still valid.
But keep the parent F1 context and rebuild F2 from that context.
```

### 9.4 F3 completion closes the chain directionally

After F3 completes:

- do not seek F4,
- do not restart F1 in the same direction within the same chain,
- treat continued same-direction movement as F3 extension,
- wait for the smallest confirmed opposite F1 to lock F3.

---

## 10. Duplicate and Identity Rules

### 10.1 Duplicate definition

Two structures are duplicates only if all relevant identity fields match exactly.

Identity must include both time and price. A tiny difference in time or price makes a different structure.

Recommended identity tuple:

```text
structure_kind
f_level
direction
origin.time
origin.price
leg1.time
leg1.price
waist.time
waist.price
leg2.time
leg2.price
scale_L
parent_sequence_id
```

If all of these match, there should be only one visible sequence/event.

If any field differs, even slightly, it is a distinct sequence/event.

### 10.2 Node identity vs price-only identity

Do not merge by price only.

Two nodes at the same price but different times are not the same structure.

Two nodes at the same time but different prices are not the same structure.

Prefer node identity based on:

```text
time + price + kind + scale context
```

---

## 11. Rendering Contract

### 11.1 All important structures are visible

The user wants to see all live/candidate/confirmed/locked structures, not only dominant structures.

The renderer must not hide valid active sequences merely because they are smaller.

However, raw seeds and rejected structures should not appear in the main chart.

### 11.2 Line style

All flag body lines should be thin and equal weight by default.

The renderer should not make larger scales thick by default.

Recommended default:

```text
InpFixedLineWidth = 1
```

Sequence distinction should come from shade variation inside the same direction/status color family, not from line thickness.

### 11.3 Curve style

The flag body should be drawn as:

```text
Origin -> Leg1 = straight segment
Leg1 -> Leg2 = smooth curve passing through Waist
```

The curve should not be a visibly broken chain of trendlines.

The curve is schematic. It only needs to pass through:

```text
Leg1 endpoint
Waist / correction extreme
Leg2 endpoint
```

It does not need to trace every candle.

### 11.4 Labels

Detailed labels should use option C:

```text
F1 L8 Q23
F2 L8 Q23
F3 L8 Q23
ND L8 Q23
```

Where:

- `F1/F2/F3/ND` = structure type,
- `L8` = scale/compression context,
- `Q23` = sequence id or chain id.

Origin label should be shown for now:

```text
O
```

The user may disable it later.

### 11.5 Label vertical positioning

- Peak labels go above peaks.
- Valley labels go below valleys.
- ND labels follow the terminal/end side of the ND structure and must participate in the same stacking system as F labels.

### 11.6 Label stack ordering

When multiple labels occupy the same local time/price cluster, the closest label to price should be the oldest sequence first.

Priority from closest to farthest:

```text
older sequence first
then higher F level: F3 > F2 > F1 > ND
then larger scale L
then confirmed/locked before live/candidate if needed
```

The key resolved rule is:

```text
older is closer to price
```

### 11.7 Invalidated structures

Invalidated/rejected structures are hidden from the main chart.

They can be written to audit logs but must not remain visually as if they are alive.

---

## 12. Implementation Inputs

Recommended inputs derived from this contract:

```text
InpShowCandidateFlags = true
InpShowConfirmedFlags = true
InpShowLockedF3 = true
InpShowRejectedFlags = false

InpShowOriginLabels = true
InpShowDetailedLevelLabels = true
InpShowInternalNumbers = true
InpShowNDLabels = true

InpFixedLineWidth = 1
InpUseSequenceColorShades = true

InpNDMinNodes = 3
InpNDMaxNodes = 4
InpNDMinRetracementRatio = 0.50
InpNDAllowBelowHalfCycle = false

InpF2MinSizeRatioToF1 = 1.00

InpF3Leg1ScaleMinRatioToF2 = 0.80
InpF3FlagSizeMinRatioToF2 = 0.70
InpF3SameScaleMode = OR_CONDITIONS

InpLockF3OnSmallestConfirmedOppositeF1 = true
```

---

## 13. Engineering Modules

A clean implementation should not be a single sliding-window scanner.

Recommended modules:

### 13.1 RawNodeStore

Responsibilities:

- collect raw high/low nodes,
- preserve all raw nodes,
- expose node lookup by time/price/type,
- never delete source observations.

### 13.2 ScaledNodeView

Responsibilities:

- build alternating node views,
- merge same-type consecutive nodes by extreme,
- adaptively increase `L`,
- return compressed node lists for a requested context.

### 13.3 FlagBodyBuilder

Responsibilities:

- build candidate two-leg bodies,
- update Leg1 to true pre-correction extreme,
- update Waist to true correction extreme,
- update Leg2 on extension when post-flag internal structure has not qualified,
- reject bodies whose Leg1 correction breaks Origin.

### 13.4 PostFlagCorrectionAnalyzer

Responsibilities:

- detect internal `1/2/3/4`,
- apply F1-specific middle-node restriction,
- apply F2 waist-break branch rules,
- detect ND/Hook status for 3/4-node compressed corrections,
- compute ND retracement ratio.

### 13.5 SequenceEngine

Responsibilities:

- manage F1 -> F2 -> F3 ordering,
- prevent restarting F1 inside an active sequence,
- keep F1 alive while seeking F2,
- keep F2 alive while seeking F3,
- handle F3 extension and lock.

### 13.6 Renderer

Responsibilities:

- draw only visible statuses,
- hide raw seeds and rejected structures,
- draw thin equal-width lines,
- draw smooth curves through Waist,
- stack labels deterministically,
- label F and ND with detailed identity.

### 13.7 AuditLogger

Responsibilities:

- log rejected structures,
- log invalidation reason,
- log compression level changes,
- log ND retracement ratio,
- log F3 same-scale condition pass/fail,
- log duplicate merge decisions.

---

## 14. Implementation Warning

The previous failure mode was caused by treating every alternating four-node window as a flag.

That approach is invalid.

A flag must have:

```text
coherent origin
true Leg1 extreme
true Waist correction extreme
true Leg2 break
sequence context
post-flag rules according to F level
invalidation identity
```

Without those, the chart will produce orphan lines that start from nowhere and do not answer:

```text
Which flag is this?
Where did its leg start?
What sequence does it belong to?
Why is it still alive?
```

This contract exists to prevent that.
