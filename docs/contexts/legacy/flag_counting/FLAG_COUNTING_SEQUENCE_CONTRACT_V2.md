<!-- CURRENT CANON NOTICE
This file is retained as historical/context documentation. For current Phoenix implementation decisions, use:

docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting Sequence Contract V2

Status: **conceptual and implementation contract**  
Scope: Flag Counting VNext detector, renderer, audit reports, and future execution modules.  
Language: English-only technical specification.  
Primary principle: **the market is interpreted as a sequence of high/low-node geometries, not candle bodies.**

---

## 1. Purpose

This document defines the exact engineering contract for the Flag Counting model used in Decision Alpha Lab.

The purpose of this model is not to label arbitrary four-point shapes. The purpose is to maintain a coherent sequence model of market structure:

```text
F1 -> F2 -> F3 -> sequence termination
```

Each `F` is a two-leg flag body. The difference between `F1`, `F2`, and `F3` is **not** the basic two-leg geometry itself. The difference is what must happen **after** the two-leg flag body.

This document exists because the previous implementation drifted into a sliding-window pattern scanner. That is not the intended model. The correct model is a chained, scale-aware, high/low-only sequence detector.

---

## 2. Non-negotiable invariants

These are hard rules. Any detector implementation that violates them is wrong.

### 2.1 High/low-only logic

The model uses only swing high and swing low nodes.

Allowed inputs for geometry:

```text
high
low
swing high node
swing low node
node index
node time
node price
node type: HIGH or LOW
```

Ignored inputs for structure detection:

```text
open
close
candle body
candle color
whether a candle closed above or below a level
```

The logic is **close-agnostic**, not close-forbidden. If a candle closes somewhere, that fact simply has no structural meaning in this model.

### 2.2 All raw high/low nodes are preserved

The engine should not destroy raw high/low information. Raw nodes remain available for audit, debugging, compression, and scale transformation.

However, the detector may view those raw nodes through a larger `L` so that a local structure becomes readable as a compressed high/low chain.

The correct approach is:

```text
preserve raw nodes
compress/adapt nodes per scale/context
count flags on the compressed view
```

Not:

```text
delete nodes permanently
force every local node into one fixed scale
```

### 2.3 Flags are sequential

Within a single sequence and scale context, flags do not restart from `F1` after every small shape.

Correct:

```text
F1 found -> search for F2
F2 found -> search for F3
F3 found -> lock the sequence
```

Incorrect:

```text
F1 found -> next flag is another F1
F1 found -> next flag is another unrelated F1 in the same sequence
```

### 2.4 Rejected structures are not drawn on the main chart

The main chart should show:

```text
candidate/live structures
confirmed structures
terminal structures
ND/Hook labels
```

The main chart should not show:

```text
rejected candidates
invalidated structures
orphan bodies
dead origins
```

Rejected items belong in audit logs, not on the main chart.

### 2.5 Candidates are visible

The research view must show candidate/live structures. Do not hide them simply because they are not confirmed yet.

Candidate structures must be visually distinguishable from confirmed structures.

---

## 3. Terminology

### 3.1 Node

A node is a swing point derived from high/low geometry.

```text
HIGH node: a local high selected by the node engine
LOW node : a local low selected by the node engine
```

Nodes may be raw or compressed.

### 3.2 Raw node

A raw node is the smallest available high/low structure detected by the configured node engine.

Raw nodes are never conceptually discarded. They can be hidden in rendering, but they remain part of the audit source.

### 3.3 Compressed node

A compressed node is a node selected after increasing the effective `L` or scale so that the local structure can be represented with at most four readable nodes.

Compression is contextual. The same raw region may be compressed differently depending on whether we are evaluating F1, F2, F3, ND, or a larger scale.

### 3.4 Flag body

A flag body is a two-leg structure:

```text
Origin -> Leg1 -> Waist -> Leg2
```

For bullish flags:

```text
Origin = LOW
Leg1   = highest HIGH before correction
Waist  = lowest LOW correction after Leg1 and before Leg2
Leg2   = HIGH that breaks/extends the Leg1 high
```

For bearish flags:

```text
Origin = HIGH
Leg1   = lowest LOW before correction
Waist  = highest HIGH correction after Leg1 and before Leg2
Leg2   = LOW that breaks/extends the Leg1 low
```

### 3.5 Waist

The waist is the internal correction extreme inside the flag body.

For bullish flags:

```text
waist = lowest correction low after Leg1 and before Leg2
```

For bearish flags:

```text
waist = highest correction high after Leg1 and before Leg2
```

The waist must be updated while the correction is still developing.

### 3.6 Internal 1/2

Internal `1` and `2` are nodes formed in the correction after the two-leg flag body is formed.

For bullish structures:

```text
After Leg2, the correction must form at least two same-side correction nodes.
Node 2 must be lower than Node 1.
A counter-node/high exists between 1 and 2.
```

In simplified bullish notation:

```text
Leg2 high
-> correction low = 1
-> intervening high
-> deeper correction low = 2
```

For bearish structures:

```text
After Leg2, the correction must form at least two same-side correction nodes.
Node 2 must be higher than Node 1.
A counter-node/low exists between 1 and 2.
```

In simplified bearish notation:

```text
Leg2 low
-> correction high = 1
-> intervening low
-> higher correction high = 2
```

If more than two correction nodes appear, the node count must still be compressed so that the readable structure has no more than four nodes.

### 3.7 ND / Hook

ND, also called Hook, is a non-flag cyclic or hook phase.

ND is detected when the local high/low node structure has three or four readable nodes after applying adaptive `L` compression.

Two nodes are not ND.

More than four nodes are not directly accepted; `L` must be increased until the structure becomes four nodes or fewer.

---

## 4. Direction model

Every flag has a direction.

### 4.1 Bullish flag

A bullish flag has this high/low skeleton:

```text
LOW  -> HIGH -> LOW  -> HIGH
O       L1      W       L2
```

Requirements:

```text
Leg1 high is above Origin low
Waist low is above Origin low for F1 validity
Leg2 high breaks or extends Leg1 high
```

### 4.2 Bearish flag

A bearish flag has this high/low skeleton:

```text
HIGH -> LOW  -> HIGH -> LOW
O       L1      W       L2
```

Requirements:

```text
Leg1 low is below Origin high
Waist high is below Origin high for F1 validity
Leg2 low breaks or extends Leg1 low
```

---

## 5. Flag body construction

### 5.1 Origin selection

An F1 origin must come from one of two contexts:

```text
1. after an ND/Hook phase
2. from the terminal/end context of an opposite-direction F sequence
```

An F1 must not start randomly in the middle of an already running move.

For bullish F1:

```text
origin should be a valid LOW after ND or after an opposite bearish sequence endpoint
```

For bearish F1:

```text
origin should be a valid HIGH after ND or after an opposite bullish sequence endpoint
```

### 5.2 Leg1 selection

Leg1 is not the first minor high/low after origin. Leg1 is the real extreme before the corrective phase.

For bullish flags:

```text
Leg1 = highest HIGH before the correction that forms the waist
```

For bearish flags:

```text
Leg1 = lowest LOW before the correction that forms the waist
```

If multiple same-side raw nodes appear before the correction, they are not independent Leg1 points. They are candidates for the same Leg1, and the most extreme one is selected.

### 5.3 Waist selection

Waist must be continuously updated while correction develops.

For bullish flags:

```text
If a lower correction low appears before Leg2 confirms, update waist to that lower low.
```

For bearish flags:

```text
If a higher correction high appears before Leg2 confirms, update waist to that higher high.
```

The detector must not freeze the first correction point as the waist if a deeper valid correction appears later.

### 5.4 Leg2 selection and extension

Leg2 is the node that breaks or extends the Leg1 extreme.

For bullish flags:

```text
Leg2 = HIGH that breaks above Leg1 high
```

For bearish flags:

```text
Leg2 = LOW that breaks below Leg1 low
```

If the flag body has been struck but the required post-flag internal 1/2 has not appeared, and price continues beyond Leg2, the new extreme remains part of the same flag body.

This is critical.

For bullish F1:

```text
O -> L1 -> W -> L2a
no valid 1/2 correction yet
price makes L2b above L2a
=> ignore L2a as final body end
=> L2b becomes the current Leg2
```

For bearish F1:

```text
O -> L1 -> W -> L2a
no valid 1/2 correction yet
price makes L2b below L2a
=> ignore L2a as final body end
=> L2b becomes the current Leg2
```

This prevents fake flags from being created from unfinished post-body corrections.

---

## 6. F1 contract

### 6.1 F1 identity

F1 is the first flag in a sequence.

F1 may start only:

```text
after ND/Hook
or after the end context of an opposite-direction F sequence
```

### 6.2 F1 flag-body invalidation

For F1, the invalidation of the flag body is the waist.

For bullish F1:

```text
If price hits/breaks below the F1 waist before F1 confirmation, the F1 candidate is invalidated.
```

For bearish F1:

```text
If price hits/breaks above the F1 waist before F1 confirmation, the F1 candidate is invalidated.
```

Important distinction:

```text
F1 invalidation = waist
F2 invalidation = beginning of Leg1 / origin
F3 completion = two-leg flag body
```

### 6.3 F1 internal 1/2 requirement

After the F1 flag body forms, F1 must produce internal 1/2 before it can be confirmed.

For bullish F1:

```text
After Leg2, correction forms 1 and 2.
2 must be below 1.
There must be an intervening high between 1 and 2.
That intervening high must NOT be above the F1 Leg2 / flag endpoint.
```

For bearish F1:

```text
After Leg2, correction forms 1 and 2.
2 must be above 1.
There must be an intervening low between 1 and 2.
That intervening low must NOT be below the F1 Leg2 / flag endpoint.
```

### 6.4 F1 confirmation

F1 is confirmed when:

```text
1. F1 flag body exists
2. internal 1/2 or a compressed higher-node correction exists before F1 waist invalidation
3. price returns and hits/breaks the F1 flag endpoint using high/low geometry
```

For bullish F1:

```text
confirmation = high/low node action that returns above/beyond the F1 Leg2 endpoint after valid internal 1/2
```

For bearish F1:

```text
confirmation = high/low node action that returns below/beyond the F1 Leg2 endpoint after valid internal 1/2
```

### 6.5 F1 when no internal 1/2 appears

If F1 flag body forms but the market does not produce internal 1/2 and instead continues beyond Leg2:

```text
the move remains part of the same F1 Leg2 extension
previous Leg2 endpoint is replaced by the new more extreme endpoint
F1 is not confirmed yet
F2 must not start yet
```

### 6.6 F1 with more than two correction nodes

If the correction after F1 Leg2 produces more than two nodes:

```text
increase effective L until the correction compresses to four or fewer readable nodes
```

If the compressed structure has three or four nodes:

```text
label that region as ND/Hook
also label the internal sequence numbers if applicable
```

Two nodes are not ND.

---

## 7. F2 contract

### 7.1 F2 starts after confirmed F1

F2 must not start before F1 is confirmed.

Correct:

```text
F1 candidate -> not confirmed -> do not create F2 yet
F1 confirmed -> search for F2
```

### 7.2 F2 origin

F2 begins from the end of the correction after the F1 two-leg flag body.

More precisely:

```text
F2 origin = the endpoint of the F1 post-flag correction sequence that produced 1/2 or more
```

This is not necessarily the first correction node. It is the terminal/deeper correction node after the F1 body that establishes the valid post-F1 correction context.

For bullish F1 leading to bullish F2:

```text
F2 origin is the lower/deeper correction endpoint after F1 Leg2, i.e. the point corresponding to F1 internal 2 or the compressed terminal correction node.
```

For bearish F1 leading to bearish F2:

```text
F2 origin is the higher/deeper correction endpoint after F1 Leg2, i.e. the point corresponding to F1 internal 2 or the compressed terminal correction node.
```

### 7.3 F2 flag body

F2 itself is still a two-leg flag body:

```text
Origin -> Leg1 -> Waist -> Leg2
```

The flag-body geometry is the same as any flag. The difference is in the post-flag rules.

### 7.4 F2 invalidation

For F2, the invalidation is the beginning of Leg1 / origin, not the waist.

For bullish F2:

```text
If price hits/breaks below the F2 origin, F2 is invalidated.
```

For bearish F2:

```text
If price hits/breaks above the F2 origin, F2 is invalidated.
```

When F2 invalidates:

```text
F2 disappears
F1 parent remains alive if F1 itself is still valid
The system continues searching for F2 from the F1 context
The sequence does not abandon F2 search while F1 remains alive
```

### 7.5 F2 waist-break branch

Unlike F1, F2 may break its own waist without being invalidated, as long as it does not hit its own origin.

If F2 breaks its waist but not its origin, that creates a waist-break branch.

The branch is interpreted as:

```text
internal 1 = F2 waist
internal 2 = node that breaks F2 waist
```

This branch is still part of F2 context.

### 7.6 F2 confirmation

F2 is confirmed when:

```text
1. F2 flag body exists
2. F2 creates internal 1/2 or more after its flag body
3. F2 may break its waist during this process, but must not break its origin
4. price returns and breaks the F2 flag endpoint using high/low geometry
```

### 7.7 F2 size requirement

F2 must be at least the size of F1.

Size is defined as the flag body displacement from the beginning of Leg1 to the end of Leg2.

For bullish flags:

```text
size = abs(Leg2 high - Origin low)
```

For bearish flags:

```text
size = abs(Origin high - Leg2 low)
```

The implementation should expose this as a rule:

```text
F2.size >= F1.size
```

A future input may allow this threshold to be relaxed or scaled.

---

## 8. F3 contract

### 8.1 F3 starts after F2

F3 is searched only after F2 exists in the sequence.

Correct sequence:

```text
F1 confirmed -> F2 search
F2 valid/confirmed context -> F3 search
```

### 8.2 F3 flag body is enough

F3 does not need the same post-flag correction logic as F1 and F2.

For F3:

```text
The two-leg flag body is enough to classify it as F3.
```

### 8.3 F3 completion

When F3 completes its flag body:

```text
The sequence is considered complete.
The sequence becomes locked.
The sequence should no longer be deleted from the chart even if the entire movement reverses later.
```

### 8.4 F3 extension

After F3 completes, the rest of the same-direction movement is considered F3 extension.

For bullish F3:

```text
Any further bullish extension before the smallest opposite F1 is treated as part of F3 extension.
```

For bearish F3:

```text
Any further bearish extension before the smallest opposite F1 is treated as part of F3 extension.
```

### 8.5 Sequence termination after F3

After F3 completes:

```text
No F4 is created.
The sequence is locked.
The next major structural process begins only after the smallest opposite F1 appears.
```

The exact engineering definition of `smallest opposite F1` remains an open item and must be formalized before production execution logic.

---

## 9. ND / Hook contract

### 9.1 ND is high/low-node based

ND uses only high/low nodes.

It does not use:

```text
close
open
body
candle color
close beyond level
```

### 9.2 ND node count

ND is recognized when the compressed node sequence has:

```text
3 nodes
or 4 nodes
```

Two nodes are not ND.

More than four nodes must be compressed by increasing `L` until the region becomes readable as four or fewer nodes.

### 9.3 Adaptive L for ND

For ND detection:

```text
initial L for the source/root node = 2
L for the origin/source is not increased
increase L for the local structure until node count <= 4
```

If after compression the node count is:

```text
3 or 4 => ND / Hook
2      => not ND
> 4    => keep increasing L or mark unresolved in audit
```

### 9.4 ND 50% cycle rule

By default, ND is accepted only when it passes the 50% cycle rule.

The cycle is measured with high/low geometry from:

```text
start node -> extreme reached by the cycle -> current/terminal cycle point
```

The rule is:

```text
The terminal node must have moved at least 50% of the start-to-extreme range.
```

This is not based on close.

It is based only on high/low node range.

### 9.5 Input for accepting below-50 ND

The implementation must support an input that allows below-50% ND to be accepted for research.

Default:

```text
accept_below_50_percent_nd = false
```

Research option:

```text
accept_below_50_percent_nd = true
```

### 9.6 ND overlap with F

ND may be detected inside or overlapping a flag.

Both may be displayed if both exist.

ND should remain text-only by default to avoid chart noise.

### 9.7 ND rendering

ND should be drawn as a text label:

```text
ND
```

It should participate in the same label stacking system as F labels.

It should not draw additional body lines by default.

---

## 10. Node compression and scale logic

### 10.1 All highs/lows are kept

The system preserves all high/low nodes.

### 10.2 Compression is contextual

The system may merge or compress nodes when a local structure has too many nodes for the current interpretation.

The compression objective is:

```text
Represent the region with at most four readable nodes.
```

### 10.3 Same-side node compression

If several same-side nodes appear consecutively in a compressed context:

For bullish upward impulse:

```text
multiple highs before correction -> keep the highest high as Leg1
```

For bearish downward impulse:

```text
multiple lows before correction -> keep the lowest low as Leg1
```

For correction:

```text
bullish correction lows -> keep the lowest low as waist/control point
bearish correction highs -> keep the highest high as waist/control point
```

### 10.4 Compression must not hide raw audit data

Compression is a view, not data destruction.

The detector should be able to report:

```text
raw node ids used
compressed node ids selected
L used for compression
reason for compression
```

---

## 11. Sequence model

### 11.1 Sequence identity

A sequence is a chain:

```text
Sequence(direction, scale_context): F1 -> F2 -> F3
```

### 11.2 Sequence progression

Valid progression:

```text
No sequence
-> ND or opposite-end context
-> F1 candidate
-> F1 confirmed
-> F2 candidate
-> F2 confirmed/valid
-> F3 candidate
-> F3 complete
-> sequence locked
```

### 11.3 No restart inside same sequence

After F1, the next same-sequence flag is F2.

After F2, the next same-sequence flag is F3.

The detector must not reclassify the next flag after F1 as another F1 inside the same chain.

### 11.4 Parent-child continuity

If a child fails, the parent remains alive if its own invalidation has not been hit.

For example:

```text
F1 confirmed
F2 candidate starts
F2 origin is hit
=> F2 is invalidated and removed
=> F1 remains alive
=> continue searching for F2 in the F1 context
```

This is not a total sequence reset.

### 11.5 Dead origins

If a candidate hits its invalidation origin, that origin is dead for that candidate.

It should not be reused to resurrect the same failed candidate.

However, the parent context may still generate a new child candidate later from a valid continuation point.

---

## 12. Invalidation model

### 12.1 F1 invalidation

F1 invalidation is the waist.

For bullish F1:

```text
hit/break below waist => F1 invalid
```

For bearish F1:

```text
hit/break above waist => F1 invalid
```

### 12.2 F2 invalidation

F2 invalidation is the beginning of its first leg / origin.

For bullish F2:

```text
hit/break below F2 origin => F2 invalid
```

For bearish F2:

```text
hit/break above F2 origin => F2 invalid
```

If F2 invalidates, F1 remains alive if F1 itself has not invalidated.

### 12.3 F3 completion instead of invalidation

F3 is not governed by the same post-flag invalidation logic.

When F3 completes its two-leg body:

```text
F3 is complete
sequence is locked
later reversal does not delete the completed F3
```

---

## 13. Candidate, confirmed, terminal, rejected

### 13.1 Candidate

A candidate is a structure currently being evaluated.

Candidate structures must be visible in research view.

### 13.2 Confirmed

Confirmed means the structure met its post-flag confirmation requirement.

For F1 and F2, confirmation requires post-flag internal 1/2 logic and then break of the flag endpoint.

### 13.3 Terminal

Terminal means F3 has completed and the sequence is locked.

### 13.4 Rejected

Rejected means invalidated or structurally failed.

Rejected structures should not be shown on the main chart.

They should be logged in audit output.

---

## 14. Duplicate sequence handling

If two sequences have exactly the same structural identity, they should not be duplicated.

Structural identity includes:

```text
direction
F level
origin node
leg1 node
waist node
leg2 node
internal 1/2 nodes if applicable
scale context
parent sequence identity
```

If every relevant field is exactly the same:

```text
render one sequence
optionally include multiple scale labels in the text
```

If even one meaningful structural field differs:

```text
treat them as different sequences
```

---

## 15. Rendering contract

### 15.1 Show all valid visible structures

The user wants to see all non-rejected structures.

Visible structures:

```text
candidate/live F structures
confirmed F structures
terminal F3 sequences
ND/Hook labels
```

Hidden from main chart:

```text
rejected structures
invalidated candidates
orphan bodies
unowned dead lines
```

### 15.2 Uniform line width

All flag body lines should have the same thin width by default.

The renderer should not make higher scales thick by default.

Default:

```text
line_width = 1
```

### 15.3 Sequence color shades

Different sequences should use slightly different shades within the same color family.

Meaning should remain stable:

```text
bullish candidate  -> bullish candidate family
bullish confirmed  -> bullish confirmed family
bearish candidate  -> bearish candidate family
bearish confirmed  -> bearish confirmed family
F3 terminal        -> terminal family
ND                 -> ND family
```

The shade differentiates sequence identity, not semantic class.

### 15.4 Label content

The preferred label mode is detailed option C:

```text
F1 L8 Q23
F2 L8 Q23
F3 L8 Q23
ND L8
```

Where:

```text
F1/F2/F3 = flag level
L8       = scale or compression L
Q23      = sequence id
```

### 15.5 Origin label

The renderer should show origin labels by default for debugging.

Origin label:

```text
O
```

This can be disabled later with input:

```text
show_origin_labels = false
```

### 15.6 Label placement

For peaks/high points:

```text
place text above the peak
```

For valleys/low points:

```text
place text below the valley
```

### 15.7 Label stacking order

When multiple labels cluster in the same time/price region, stack them deterministically.

Nearest to price should be:

```text
older sequence first
then larger scale / L context
then higher F level: F3 > F2 > F1 > ND
then confirmed before candidate
```

The user explicitly selected:

```text
older sequence closer to price
```

### 15.8 Curve rendering

Flag body rendering:

```text
Origin -> Leg1 = straight line
Leg1 -> Leg2  = smooth curve passing through Waist
```

The curve is schematic. It does not need to follow every candle.

It must pass through:

```text
Leg1 endpoint
true waist/correction extreme
Leg2 endpoint
```

The curve should not be drawn as a few visibly broken trendlines. It should be rendered with enough segments to look smooth.

---

## 16. Open engineering items

These items are not fully locked yet and should be finalized before production execution.

### 16.1 Same-scale requirement for F1/F2/F3

The user stated that F3 must be in the same scale as its F1 and F2.

A general same-scale rule must be defined.

Possible definitions:

```text
A. same exact L
B. same compressed node family
C. same volatility-normalized body scale
D. same parent sequence scale context
```

This requires a separate decision.

### 16.2 Smallest opposite F1 after F3

After F3 completes, the whole same-direction move is treated as F3 extension until the smallest opposite F1 appears.

The exact definition of smallest opposite F1 must be formalized.

Possible definitions:

```text
A. smallest configured L that produces a valid opposite F1
B. first opposite F1 candidate after F3 completion
C. first confirmed opposite F1 after F3 completion
D. first opposite F1 that breaks the F3 extension control point
```

### 16.3 ND below 50%

The default is ND above 50% cycle threshold.

A research input should allow below-50 ND.

The exact labeling for below-50 ND may be:

```text
ND?
ND<50
weak ND
```

This is not yet locked.

---

## 17. Implementation warning

Do not implement this as a simple sliding-window detector.

Wrong implementation style:

```text
for every 4 alternating nodes:
    draw F1
```

Correct implementation style:

```text
maintain sequence state
preserve raw nodes
compress contextually
construct F1 only from valid F1 origins
confirm F1 before F2 search
continue F2 search while F1 remains alive
construct F3 after F2
lock sequence after F3
render only non-rejected structures
```

The previous chart errors came from treating raw local alternating windows as independent flags. This contract explicitly forbids that behavior.
