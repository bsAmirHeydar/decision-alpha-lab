<!-- CURRENT CANON NOTICE
This file is retained as historical/context documentation. For current Phoenix implementation decisions, use:

docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting Concept Specification v3

Status: authoritative design contract for the next Flag Counting implementation.

This document replaces the earlier loose pattern-scanner interpretation. Flag Counting is not a collection of independent chart patterns. It is a fractal, multi-scale, multi-sequence movement grammar intended to partition market movement into ND/Hook phases and F-counting phases.

The goal is to make the engine answer, programmatically and visually:

- Are we inside ND/Hook or inside an F-counting phase?
- If inside F-counting, which F-level are we in: F1, F2, F3?
- Which scale produced this sequence?
- Where are Origin, Leg1, Waist, Leg2, Internal 1, Internal 2, confirmation, and invalidation?
- Is the structure live, confirmed, failed, extended, reinterpreted, or terminal?

## 1. Core worldview

The market is treated as a nested movement language. A visible move is not simply a trend, pullback, and continuation. It is counted as a sequence of flags across one or more scales:

- ND/Hook phase: cyclic compression, hook formation, or non-flag movement.
- F-counting phase: F1 -> F2 -> F3.
- Fractal overlay: multiple sequences can exist in parallel across different scales.

The system must not behave as a global single-chain engine. It must maintain a registry of multiple active sequences. Each valid F1 opens a new sequence. That sequence then expects F2. After confirmed F2, it expects F3. Meanwhile, other scales can create their own sequences.

## 2. Why the earlier implementation failed

The earlier detector failed because it was still a pattern scanner:

1. It scanned every group of nodes as a possible F1.
2. It attempted to create F2/F3 from all discovered F1/F2 candidates.
3. It either over-drew overlapping structures or became too strict and drew nothing.
4. It did not maintain persistent sequence state.
5. It did not represent ND/Hook as a market phase.
6. It used one scale or treated scales as independent scans rather than parallel sequence layers.

The correct engine must be sequence-first, stateful, multi-scale, and auditable.

## 3. Terms and definitions

### 3.1 Node

A node is a structurally meaningful swing high or swing low produced by a swing detector at scale `L`.

Each node must store:

- index
- time
- price
- kind: high or low
- scale L
- source timeframe
- local confirmation depth

A node is not just a visual pivot. It is the atomic unit of the Flag Counting grammar.

### 3.2 Scale L

`L` controls the granularity of node detection. Small L creates smaller, more reactive nodes. Large L creates broader, cleaner structure.

Flag Counting is fractal, so multiple L values can be active at the same time. Example active set:

- L=2
- L=3
- L=5
- L=8
- L=13
- L=21

The engine must support adaptive L for ND/Hook detection. If a hook contains too many internal nodes, L is increased until the hook is representable by 3 or 4 nodes.

### 3.3 Direction

A flag sequence can be bullish or bearish.

Bullish body:

- Origin is a low.
- Leg1 ends at a high.
- Waist is a corrective low.
- Leg2 ends at a high.

Bearish body:

- Origin is a high.
- Leg1 ends at a low.
- Waist is a corrective high.
- Leg2 ends at a low.

Direction determines geometry, invalidation, internal count interpretation, and rendering color.

### 3.4 Origin

Origin is the start of the current F body.

For F1, Origin must come from the beginning of a trend leg, not from a random unowned middle point. Valid F1 origins usually appear after ND/Hook, after a completed opposite-direction F sequence, or after a reset condition.

For F2, Origin is the Internal 2 of the parent F1, or a later valid internal count point if the parent count has extended and the lower correction point is updated according to the sequence rules.

For F3, Origin is the Internal 2 of the parent F2.

### 3.5 Leg1

Leg1 is the first impulse from Origin in the sequence direction.

Bullish:

- Origin low -> Leg1 high.

Bearish:

- Origin high -> Leg1 low.

### 3.6 Waist

Waist is the corrective pivot after Leg1 and before Leg2.

Bullish:

- Waist is a low after Leg1.
- It must not be behind the Origin while the F1 body is valid.
- For F1, if Waist is broken after the body is built, F1 invalidates.

Bearish:

- Waist is a high after Leg1.
- It must not be behind the Origin while the F1 body is valid.
- For F1, if Waist is broken after the body is built, F1 invalidates.

For F2 and F3, Waist break is not automatically invalidation. It can become the waist-break branch:

- Internal 1 = Waist.
- Internal 2 = the node that breaks Waist.

The continuation-level invalidation boundary is Origin, not Waist.

### 3.7 Leg2

Leg2 is the second impulse in the same direction as Leg1.

Bullish:

- Leg2 high must break or exceed Leg1 high.

Bearish:

- Leg2 low must break or exceed Leg1 low in the bearish direction.

Leg2 may extend while the structure is live. If only Internal 1 forms and price returns to extend the direction, the move is still considered part of Leg2 until the Internal 2 rule is satisfied.

### 3.8 Internal 1 and Internal 2

Internal 1/2 are post-Leg2 counting points. They are not Leg1/Leg2 labels.

For F1 bullish:

- Internal 1 = first low after Leg2.
- Internal 2 = later low lower than Internal 1, still above Waist.
- Internal 1 and 2 must form before the confirming Leg2 rebreak.

For F1 bearish:

- Internal 1 = first high after Leg2.
- Internal 2 = later high higher than Internal 1, still below Waist.
- Internal 1 and 2 must form before the confirming Leg2 rebreak.

If only Internal 1 forms and price returns to extend Leg2, the structure has not entered the post-Leg2 correction. It remains in the Leg2 extension phase.

For F2/F3 bullish:

- Internal 1/2 may form like F1.
- Or Waist can be broken while Origin remains protected:
  - Internal 1 = Waist.
  - Internal 2 = the waist-breaking node.
- Leg2 can extend above its previous endpoint before Internal 2 is finalized.

For F2/F3 bearish:

- Internal 1/2 may form like F1.
- Or Waist can be broken while Origin remains protected:
  - Internal 1 = Waist.
  - Internal 2 = the waist-breaking node.
- Leg2 can extend below its previous endpoint before Internal 2 is finalized.

### 3.9 Confirmation

For F1 and F2:

- Confirmation occurs when price rebreaks its own Leg2 endpoint before invalidation.

For F1, Internal 1/2 must have formed before the confirming Leg2 rebreak.

For F2, the sequence may extend beyond Leg2 before Internal 2 is finalized. A later pullback into Internal 2 can complete the branch, and the earlier or later Leg2 extension can be interpreted under the continuation logic.

For F3:

- F3 is special and terminal-like.
- Once F3 gives its two-leg body, the F3 structure is considered established/locked for that sequence.
- F3 may not need a later Leg2 rebreak like F1/F2.
- The post-F3 move can reverse and begin the next market phase.

### 3.10 Invalidation

F1 invalidation:

- F1 invalidates if its Waist is broken.
- If F1 Waist breaks, the following F-levels derived from that F1 fail too.
- The sequence may need to be recounted as a new F1 with a new Waist, or treated as ND at that scale.

F2 invalidation:

- F2 invalidates only if its Origin is broken.
- Waist break is not invalidation for F2. It can be the F2 waist-break branch.

F3 invalidation:

- F3 does not behave like F1/F2 after the two-leg body is complete.
- Once the two-leg F3 body is established, the sequence is considered to have done its job and becomes terminal/locked.
- Post-F3 movement may reverse, transition, or start new sequences.

### 3.11 Size

Flag body size is measured as price distance:

`size = abs(Leg2.price - Origin.price)`

No log, percent, ATR, or volatility normalization is used in the first implementation.

F2 size rule:

- F2 size must be greater than or equal to its parent F1 size.

F3 size rule:

- F3 does not need to satisfy the same parent-size symmetry rule relative to F2.

## 4. F1 grammar

F1 is the root flag of a sequence.

### 4.1 Bullish F1

Required body:

1. Origin low.
2. Leg1 high above Origin.
3. Waist low after Leg1 and above Origin.
4. Leg2 high breaking Leg1.

Post-body requirement:

1. Internal 1 low after Leg2.
2. Internal 2 lower than Internal 1 but above Waist.
3. Rebreak Leg2 after Internal 2.

Confirmation:

- Leg2 rebreak after Internal 1/2 and before Waist break.

Invalidation:

- Waist break.

If only Internal 1 forms and price moves upward again, the F1 remains in Leg2 extension. It is not yet in completed post-Leg2 correction.

### 4.2 Bearish F1

Required body:

1. Origin high.
2. Leg1 low below Origin.
3. Waist high after Leg1 and below Origin.
4. Leg2 low breaking Leg1.

Post-body requirement:

1. Internal 1 high after Leg2.
2. Internal 2 higher than Internal 1 but below Waist.
3. Rebreak Leg2 after Internal 2.

Confirmation:

- Leg2 rebreak after Internal 1/2 and before Waist break.

Invalidation:

- Waist break.

## 5. F2 grammar

F2 is mandatory after a valid F1 unless the parent F1 invalidates or the sequence is recounted.

F2 Origin:

- Internal 2 of parent F1.
- If F1 is still extending and Internal 2 is not finalized, F2 is not started yet; the parent F1 remains live.

### 5.1 F2 body

F2 body uses the same Origin -> Leg1 -> Waist -> Leg2 shape as F1.

Bullish F2:

- Origin low from parent F1 Internal 2.
- Leg1 high.
- Waist low.
- Leg2 high breaking Leg1.

Bearish F2:

- Origin high from parent F1 Internal 2.
- Leg1 low.
- Waist high.
- Leg2 low breaking Leg1.

### 5.2 F2 invalidation

F2 invalidates if its Origin is broken.

If F2 Origin is broken while the parent F1 Waist is not broken, this means the attempted F2 was being counted incorrectly. The child sequence must be recounted from the correct live movement. It does not necessarily destroy parent F1.

If parent F1 Waist breaks, parent F1 fails and all child F-levels derived from it fail too.

### 5.3 F2 confirmation

F2 confirms by rebreaking its own Leg2 before its Origin invalidation.

F2 can extend substantially. There is no maximum extension. While F2 is live, it is drawn as pending/live with its pending direction color.

### 5.4 F2 waist-break branch

If F2 Waist is broken while Origin remains protected:

- Internal 1 = Waist.
- Internal 2 = the node that breaks Waist.

This is valid F2 counting, not invalidation.

F2 may also use the normal F1-like internal 1/2 branch if Waist is not broken.

### 5.5 F2 size symmetry

F2 body size must be at least the parent F1 body size:

`F2.size >= F1.size`

This is a strict rule.

## 6. F3 grammar

F3 is mandatory after confirmed F2 and represents the third movement count in the sequence.

F3 Origin:

- Internal 2 of parent F2.

F3 body:

- Origin -> Leg1 -> Waist -> Leg2.

F3 special rule:

- After the two-leg F3 body is formed, the sequence is considered structurally complete/locked.
- Market can reverse after F3.
- The movement after F3 body completion should be highlighted differently because it is terminal/transition behavior.

F3 does not require parent-size symmetry relative to F2.

F3 may use the same waist-break branch as F2 before its terminal state is established.

## 7. Extension and reinterpretation

Extension is not failure.

If a structure is waiting for Internal 2 and price continues in the direction of Leg2, the current F body is extended. The Leg2 endpoint is updated.

F1 can be fixed within its scale once it confirms with valid Internal 1/2. But if it breaks Waist or continues without satisfying the Internal 1/2 requirement, it may need to be extended or recounted.

If F1 Waist breaks, it is not a valid F1 in that scale. The sequence must be recounted, or the movement is treated as ND at that scale.

For F2, if the attempted child breaks its Origin but parent F1 Waist remains intact, the child F2 count is wrong and must be recalculated. The parent can remain valid.

## 8. ND / Hook grammar

ND means a hook/cycle phase where no valid F structure can be formed at the current scale, or where the market is forming a non-flag cyclic compression.

ND is not a decorative annotation. It is part of the market partition.

ND characteristics:

- More than two nodes.
- Usually three or four nodes around an extreme.
- It does not require a 90 percent retracement.
- The extreme condition should be at least above 50 percent of the relevant cycle range.
- It can be small or large.
- Many F structures can live inside broader ND structures at other scales.

Adaptive L rule for ND:

1. Start from small L, e.g. L=2.
2. Count hook nodes.
3. If the hook has more than four nodes, increase L.
4. Continue until the hook can be represented by three or four nodes.
5. That L becomes the ND/Hook scale for that phase.

ND closes when:

- A valid F1 forms and confirms after the potential ND; or
- The ND node cycle itself completes according to the 3/4-node hook logic.

If F2 is not visible yet after F1, the sequence should extend and continue searching for F2 in that scale. The area can also be interpreted as ND in another scale.

## 9. Multi-scale and multi-sequence design

Flag Counting is fractal.

Multiple scales must be active:

- F1 at L=3 can coexist with F1/F2/F3 at L=8.
- Child F2/F3 can use a different scale from its parent.
- There is no hard scale restriction initially.
- Symmetry still applies: F2 must be at least as large as F1 in price movement.

Multiple sequences are allowed:

- Every valid F1 starts a new sequence.
- Existing sequences keep updating.
- The engine keeps scanning for new valid, non-duplicate, non-overlapping sequence origins.
- If a candidate is the same structure across scales, it should be deduplicated.
- If it differs structurally, it can remain as a separate fractal sequence.

Inside one scale:

- Parallel sequences are allowed if they are not just duplicates or the same ownerless middle start.
- F1 Origin must come from the true beginning of a trend leg: after ND, after a completed opposite-side F, or after a valid reset boundary.

Between scales:

- Overlap is allowed unless two structures are essentially identical.

## 10. Rendering contract

Rendering is for clarity, not for showing every internal path.

For each F body:

- Origin -> Leg1: straight trend line.
- Leg1 -> Waist -> Leg2: one smooth curve.
- The belly of the curve should be tangent to or visually touch the Waist correction.
- F1/F2/F3 label: small.
- Internal 1/2 labels: small numeric labels only.
- No line should be drawn from Leg2 to Internal 1/2 by default.

Color contract:

- Direction and status create four colors:
  - bullish pending/live
  - bullish confirmed/locked
  - bearish pending/live
  - bearish confirmed/locked
- F3 post-body terminal behavior should have a special visual style or color because after F3 the market may reverse.

Scale visual weight:

- All scales can be displayed.
- Larger scales should have slightly larger labels and thicker lines.
- Smaller scales should remain thin and subtle.

Object lifecycle:

- Objects created by the experiment must be removed on deinit.
- Renderer must never leave orphan default `Text` labels.
- Rendering should be optional by mode: clean visual mode, debug visual mode, audit mode.

## 11. Required queryable state

The main output of the engine must not only be visual. Code must be able to query the current state for any symbol/timeframe/scale set.

Required state fields:

- phase: ND or F
- scale L
- sequence id
- parent sequence id
- direction
- level: F1, F2, F3
- position inside level:
  - waiting_origin
  - building_leg1
  - building_waist
  - building_leg2
  - waiting_internal1
  - waiting_internal2
  - waiting_rebreak
  - confirmed
  - invalidated
  - terminal_f3
- Origin
- Leg1
- Waist
- Leg2
- Internal 1
- Internal 2
- confirmation point
- invalidation boundary
- size
- parent size
- live extension state
- ND/hook state

## 12. Audit and logging

Logging should be off by default but complete when enabled.

Each accepted or rejected candidate should be auditable with:

- symbol
- timeframe
- scaleL
- sequenceId
- parentId
- candidateId
- level
- direction
- status
- phase
- origin index/time/price
- leg1 index/time/price
- waist index/time/price
- leg2 index/time/price
- internal1 index/time/price
- internal2 index/time/price
- confirm index/time/price
- invalid index/time/price
- invalidation rule
- size
- parent size
- size ratio
- extension count
- branch type: normal_internal12, waist_break, terminal_f3, ND
- reject reason
- transition reason

The engine should support:

- visual mode: accepted states only.
- audit mode: accepted + rejected candidates + reasons.
- snapshot mode: current state only.
- replay mode: state evolution over bars/nodes.

## 13. Implementation architecture

The final engine should be modular:

1. Node Engine
   - produces multi-scale nodes.

2. ND/Hook Engine
   - detects adaptive L hooks and ND phases.

3. F Body Builder
   - builds Origin -> Leg1 -> Waist -> Leg2 bodies.

4. Internal Count Engine
   - finds Internal 1/2 rules for F1 and F2/F3.

5. Continuation Engine
   - creates child F2/F3 from parent Internal 2.

6. Sequence Registry
   - stores active, confirmed, invalidated, terminal sequences.

7. Conflict Resolver
   - deduplicates identical structures and controls same-scale overlap.

8. State Query API
   - returns the current ND/F state for use by strategies and reports.

9. Renderer
   - draws clean body-only visuals with optional debug layers.

10. Audit Logger
   - emits full trace only when requested.

## 14. Algorithmic skeleton

At each update:

1. Build nodes for all active scales.
2. Update existing sequences first.
3. For each live F1:
   - extend Leg2 if needed.
   - detect Internal 1/2.
   - confirm by Leg2 rebreak only after F1 Internal 1/2 exists.
   - invalidate by Waist break.
4. For each confirmed F1 with Internal 2:
   - spawn or update F2 from that Internal 2.
5. For each live F2:
   - protect Origin.
   - allow Waist-break branch.
   - allow Leg2 extension.
   - confirm by Leg2 rebreak before Origin break.
   - enforce F2 size >= F1 size.
6. For each confirmed F2 with Internal 2:
   - spawn or update F3 from that Internal 2.
7. For each live F3:
   - protect Origin until body formation.
   - allow Waist-break branch.
   - once two-leg body is established, mark terminal/locked.
   - render post-F3 movement with special style if enabled.
8. Detect ND/Hook phases for areas not owned by an F sequence at that scale.
9. Scan for new F1 roots only where the origin is legitimate: after ND, after opposite completed F, or after reset.
10. Resolve duplicates and overlaps.
11. Emit queryable state, optional logs, and renderer objects.

## 15. Non-negotiable design rules

1. Do not return to F1 immediately after a valid F1 within the same sequence.
2. F2 is mandatory after F1 unless F1 invalidates or the count is reinterpreted.
3. F3 is mandatory after F2, but F3 is terminal-like after its two-leg body.
4. F1 invalidation is Waist break.
5. F2 invalidation is Origin break.
6. F3 terminal state does not behave like normal invalidation after body completion.
7. F2 must be at least as large as F1 by price body size.
8. F3 does not require the F2 parent-size rule.
9. Multiple scales and sequences can coexist.
10. The chart should be a clean visualization of accepted state, not a dump of every candidate.
