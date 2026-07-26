<!-- CURRENT CANON NOTICE
This file is retained as historical/context documentation. For current Phoenix implementation decisions, use:

docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting Concept Specification v2

Status: concept contract, not implementation.
Language: English.
Purpose: freeze the full F-counting logic before any new code is written.

This document converts the latest discussion into an engineering contract for the next implementation of the Flag Counting experiment. The key correction is that Flag Counting is not a loose pattern scanner. It is a fractal, multi-scale, multi-sequence market-state system.

---

## 1. Core thesis

The market movement should be interpreted through two structural families:

1. F-counting phases: directional flag-count sequences.
2. ND / Hook phases: non-hunted hook or cycle phases, often appearing when a clean F cannot be formed at the current scale.

The goal is not to draw every possible flag-like pattern. The goal is to understand the current market state:

- Are we inside ND / Hook?
- Are we inside an F phase?
- If inside F, are we in F1, F2, F3, or a live extension?
- Which scale owns this reading?
- Which sequence owns this reading?
- Where exactly are we inside that sequence?

The engine must support parallel sequences and multiple scales. A single global chain is not enough.

---

## 2. Terminology

### 2.1 Node

A node is a structural high or low at a specific scale. Nodes are not fixed forever; they depend on the selected scale `L`. A smaller `L` creates a finer node stream. A larger `L` creates a coarser node stream.

### 2.2 Scale `L`

Scale is the structural sensitivity used to create nodes. The engine should support multiple active scales. There is no fixed restriction that parent and child must share the same scale.

### 2.3 Sequence

A sequence is an owned F-counting thread. It has its own:

- sequence id
- scale
- direction
- parent sequence id
- current F level
- origin
- leg1
- waist
- leg2
- internal 1
- internal 2
- confirmation point
- invalidation boundary
- live / confirmed / invalid / completed state

A sequence can be live for a long time. It can extend. It should not be deleted just because the next F level is not immediately available.

### 2.4 F body

Every F body has the same base geometry:

- Origin / start of the leg
- Leg1 endpoint
- Waist / correction point
- Leg2 endpoint

For a bullish F body:

- Origin is a low.
- Leg1 is a high.
- Waist is a low inside the body, above Origin and below Leg1.
- Leg2 is a high beyond Leg1.

For a bearish F body:

- Origin is a high.
- Leg1 is a low.
- Waist is a high inside the body, below Origin and above Leg1.
- Leg2 is a low beyond Leg1.

The waist cannot fall behind the origin. If it does, the body is not a valid F body.

### 2.5 Body size

Body size is price distance only:

`size = abs(Leg2.price - Origin.price)`

No log distance, percent distance, ATR normalization, or volatility normalization is used for the core rule.

---

## 3. F1 contract

F1 is the root F of a sequence.

### 3.1 F1 body

F1 body:

`Origin -> Leg1 -> Waist -> Leg2`

### 3.2 F1 internal 1 and 2

For bullish F1:

- Internal 1 = first low after Leg2.
- Internal 2 = later low below Internal 1, while still above the F1 Waist.

For bearish F1:

- Internal 1 = first high after Leg2.
- Internal 2 = later high above Internal 1, while still below the F1 Waist.

### 3.3 F1 requires internal 1 and 2 before confirmation

For F1, Internal 1 and Internal 2 must be formed before the confirming rebreak of Leg2.

If only Internal 1 is formed and price returns toward Leg2, the movement is still considered an extension of F1 Leg2, not a separate post-Leg2 correction.

Example for bullish F1:

- Leg2 is made.
- Price creates only Internal 1.
- Price rises again.
- This is still Leg2 extension until the valid Internal 2 condition is satisfied before confirmation.

### 3.4 F1 confirmation

F1 is confirmed only when:

1. A valid F1 body exists.
2. Internal 1 and Internal 2 exist before the confirming Leg2 rebreak.
3. Price rebreaks its own Leg2 before invalidation.

### 3.5 F1 invalidation

F1 invalidation boundary is its Waist.

If the F1 Waist breaks, that F1 is invalid. Its child F levels fail with it. The old F1 should not remain as a valid F1. The engine may recount the movement from scratch, possibly with a new waist or a larger-scale structure, but the previous F1 candidate is dead.

If the start/origin of the initial leg is broken, the attempted count is completely cancelled.

### 3.6 F1 reinterpretation / extension

In the selected scale, once F1 is properly confirmed, it becomes fixed.

Before proper confirmation, if the movement continues without a valid Internal 1/2 sequence, F1 must be extended or recounted until the conditions make sense. The engine must not prematurely lock an F1 that cannot satisfy the F1 internal 1/2 requirement.

---

## 4. F2 contract

F2 is mandatory after a valid F1, unless the F1 is invalidated.

### 4.1 F2 origin

F2 starts from the corrective low/high of F1 after F1 confirmation. In the normal case, this is Internal 2 of F1.

However, if the post-F1 correction extends before the child body locks, the handoff node may be a later corrective count node, not necessarily the first candidate Internal 2. Conceptually:

`F2 Origin = the final valid post-F1 correction node that hands off into F2`

This is usually the F1 Internal 2.

### 4.2 F2 body

F2 body:

`F2 Origin -> F2 Leg1 -> F2 Waist -> F2 Leg2`

F2 uses the same body geometry as F1.

### 4.3 F2 size symmetry

F2 must be at least as large as its parent F1:

`F2 size >= F1 size`

Size is measured from Origin to Leg2 by price distance.

Before the size requirement is satisfied, the movement can be treated as live / immature F2, but it is not a locked valid F2.

### 4.4 F2 internal 1 and 2

F2 can create Internal 1 and Internal 2 like F1, but F2 is more flexible than F1.

For F2, price may extend beyond Leg2 before the full Internal 1/2 sequence is completed.

Example bullish F2:

- F2 body forms.
- Internal 1 appears.
- Price rebreaks / extends beyond F2 Leg2.
- Price later returns and forms Internal 2.
- This can still be part of the same F2 sequence.

### 4.5 F2 waist-break branch

F2 can break its own waist without invalidating, as long as its Origin is not broken.

When F2 Waist breaks, the branch can be counted as:

- Internal 1 = F2 Waist
- Internal 2 = the node that breaks the F2 Waist

This is a valid F2 branch only if F2 Origin remains protected.

### 4.6 F2 confirmation

F2 confirmation is:

`rebreak of own Leg2 before invalidation`

But because F2 can extend and build its internal counts later, the implementation must not kill the sequence merely because Leg2 extension occurs before the final internal count is clean.

### 4.7 F2 invalidation

F2 invalidation boundary is its Origin / start of its leg.

If the movement that was being interpreted as F2 breaks its own Origin but does not break the parent F1 Waist, then the current F2 count was wrong and must be recounted from the parent context. This does not automatically kill the parent F1.

If F1 Waist breaks, the parent F1 and all child F2/F3 counts are invalidated.

---

## 5. F3 contract

F3 is mandatory after F2, but its lifecycle is special.

### 5.1 F3 origin

F3 starts from the F2 handoff node, normally the Internal 2 of F2 or the equivalent final corrective handoff node.

### 5.2 F3 body

F3 body:

`F3 Origin -> F3 Leg1 -> F3 Waist -> F3 Leg2`

### 5.3 F3 does not need parent-size symmetry

F3 does not need to be larger than F2. The F2/F1 symmetry rule does not automatically apply to F3.

### 5.4 F3 completion

F3 is structurally recognized after it gives its two-leg body.

Unlike F1/F2, F3 may not rebreak its own Leg2. After F3 gives two legs, the market may reverse. This is part of the concept: after F3, the directional process may be exhausted.

The F3 Leg2 is considered counted when it is stabilized by the scale `L` node logic.

### 5.5 F3 after-body movement

The movement after the two-leg F3 body is special and should be rendered / audited differently. If price continues in the same direction after the F3 body, it is treated as an F3 extension until a new structure or reversal process starts.

### 5.6 F3 invalidation

After the F3 two-leg structure is locked, invalidation no longer has the same meaning. The F3 sequence has already done its job and the process is complete.

Before F3 body completion, origin break means the attempted F3 count was wrong and should be recounted from the parent context.

### 5.7 F3 waist-break branch

F3 can also use the waist-break branch like F2:

- Internal 1 = F3 Waist
- Internal 2 = the node that breaks the F3 Waist

But F3 remains special because it can complete after its two-leg body and then reverse without needing Leg2 rebreak confirmation.

---

## 6. Extension rules

### 6.1 Live extension is normal

An F can become much larger than initially expected. This is not a problem.

The engine must allow live extension. It must not force a new F1 just because the current F has not completed quickly.

### 6.2 Extension and smaller sequences

While a higher-level F is extending, the engine must continue scanning smaller scales. Smaller F sequences can exist inside the extension of a larger F.

This is essential because the system is fractal.

### 6.3 Recounting when the assumed child fails

After F1, F2 is mandatory. But the initially assumed F2 body can be wrong.

If F2 Origin is broken while F1 Waist is not broken, the engine should recount the F2 from the F1 context. It should not immediately create a new unrelated F1 in that same flow.

---

## 7. ND / Hook contract

ND means hook / cycle. ND can appear between F phases and can also contain smaller F structures fractally.

### 7.1 Role of ND

ND is the phase where the current scale cannot form a valid F, or where the market is building a hook-like cycle before the next F starts.

ND is not just decoration. It is part of market partitioning.

### 7.2 ND node count

ND usually closes with 3 or 4 nodes. It must have more than 2 nodes.

The extreme does not need to retrace 90%. A retracement or extreme relation above 50% can be enough.

### 7.3 Adaptive L for ND

ND detection should adapt `L`:

- Start from `L=2`.
- Count the ND / Hook nodes.
- If the hook has more than 4 nodes, increase `L`.
- Continue until the hook count becomes 3 or 4.

That selected `L` becomes the structural scale of that ND / Hook.

### 7.4 ND confirmation

ND can be considered confirmed in two ways:

1. It completes its own hook/cycle node count.
2. A following F1 starts and confirms, which confirms the preceding hook retrospectively.

### 7.5 ND and F coexist fractally

A segment can be ND at one scale while containing smaller F sequences inside it.

---

## 8. Multi-scale and parallel sequence contract

### 8.1 Multi-scale is mandatory

The engine must scan multiple scales. F structures can appear at small and large scales at the same time.

### 8.2 Child scale is unrestricted

A child F2/F3 can use a different scale from its parent. There is no scale restriction for now.

### 8.3 Parallel sequences are allowed

The engine must support parallel sequences.

When an F1 is created, it opens a sequence waiting for F2. At the same time, the engine keeps scanning for new non-overlapping or meaningfully different sequences.

### 8.4 Same-scale overlap

Inside the same scale, parallel sequences are allowed only if they are not just duplicates of the same structure. A new F1 should start from the true beginning of a trend leg, not from an ownerless mid-move.

A valid F1 start should normally be preceded by:

- ND / Hook closure, or
- the end of an opposite-direction F sequence, or
- a clear reset context.

### 8.5 Cross-scale overlap

Between different scales, overlap is allowed because the system is fractal.

If two scale readings are exactly identical, keep one. If they differ materially, keep both.

---

## 9. Rendering contract

The visual layer must stay clean.

### 9.1 Body-only rendering

For each F body, draw only:

- Origin -> Leg1 as a straight trend line.
- Leg1 -> Waist -> Leg2 as one smooth curve.
- The belly / semicircle of the curve must be tangent to, or visually touch, the Waist.
- F1 / F2 / F3 label as small text.
- Internal 1 and Internal 2 as small numeric labels only.

Do not draw extra lines from Leg2 to Internal 1/2 unless debug mode explicitly asks for it.

### 9.2 Four direction/status colors

The visual contract uses four main colors:

- Bullish pending / live
- Bullish confirmed / locked
- Bearish pending / live
- Bearish confirmed / locked

F3 post-body / terminal movement should have a special rendering style or color because it has a special lifecycle.

### 9.3 Scale visual hierarchy

All scales can be shown. Larger scales should have:

- slightly thicker lines
- slightly larger text
- stronger visual priority

Smaller scales remain thinner and lighter.

### 9.4 Deinit cleanup

The chart must remove all objects created by the Flag Counting experiment on deinitialization.

---

## 10. Engine output contract

The detector should not only draw. It must expose state to code.

For any symbol/timeframe, the engine should be able to answer:

- Are we in ND or F?
- If in F, which F level are we in?
- Which sequence owns the current state?
- Which scale owns the current state?
- What is the direction?
- Are we in Origin, Leg1, Waist correction, Leg2 extension, Internal 1/2 formation, confirmation, F3 post-body, or ND?
- What is the invalidation boundary?
- What is the confirmation boundary?
- Is the sequence live, confirmed, invalid, completed, or waiting for child?

This output is more important than the chart drawing.

---

## 11. Audit and logging contract

Detailed logs must exist but must be off by default.

When enabled, event logs should include:

- scaleL
- sequenceId
- parentId
- level
- direction
- status
- phase
- origin time/price
- leg1 time/price
- waist time/price
- leg2 time/price
- internal1 time/price
- internal2 time/price
- confirm time/price
- invalid time/price
- size
- parentSize
- sizeRatio
- invalidation boundary
- confirmation boundary
- branch type
- reason
- rejected candidate reason
- current engine state

The engine should support two modes:

1. Visual mode: accepted sequences only, clean rendering.
2. Audit mode: accepted and rejected candidates with reasons.

---

## 12. Implementation architecture

The next implementation should not patch the old scanner. It should be built as a clean modular engine.

### 12.1 Required modules

1. Multi-scale node engine
2. Adaptive ND / Hook engine
3. Sequence registry
4. F1 root builder
5. F2/F3 child builder
6. Extension and recount manager
7. Conflict resolver
8. Renderer
9. Query API
10. Audit logger

### 12.2 Implementation priority

The final target is full implementation:

- multi-scale
- parallel sequences
- ND / Hook partitioning
- F1/F2/F3 logic
- live extension
- size symmetry
- clean rendering
- queryable state
- audit logs

However, the implementation should still be built in safe internal milestones:

1. Document-only contract.
2. Data structures and query API.
3. Node engine and adaptive scale audit.
4. F1 builder with strict F1 internal rules.
5. F2 builder with mandatory continuation and size symmetry.
6. F3 builder with special terminal behavior.
7. ND / Hook engine.
8. Multi-sequence registry.
9. Multi-scale conflict resolver.
10. Renderer and chart cleanup.

---

## 13. Non-negotiable rules

1. Flag Counting is not a loose pattern scanner.
2. After F1, F2 is mandatory unless F1 is invalidated or the structure must be recounted.
3. After F2, F3 is mandatory.
4. F1 requires Internal 1 and Internal 2 before its confirming Leg2 rebreak.
5. F2 and F3 can extend beyond Leg2 before final internal count resolution.
6. F1 invalidates at Waist.
7. F2 invalidates at Origin.
8. F3 has special post-body behavior and can complete without Leg2 rebreak.
9. F2 must be at least as large as F1.
10. F3 does not require parent-size symmetry.
11. Multi-scale and parallel sequences are mandatory.
12. ND / Hook is part of the market partition, not decoration.
13. The engine output must be queryable by code, not only drawn on chart.
14. Logs must be detailed but off by default.
15. Rendering must be clean and body-only by default.

---

## 14. Remaining implementation notes

The concept is now specific enough to stop modifying the old patch chain and start a clean implementation.

The biggest engineering risk is not the F body geometry. The biggest risk is sequence ownership:

- which sequence owns a piece of movement
- when a sequence should extend
- when it should spawn a child
- when it should be recounted
- when a new parallel sequence is allowed
- when ND owns the movement

The first implementation should focus on producing correct event/state output before trying to optimize the visual layer.
