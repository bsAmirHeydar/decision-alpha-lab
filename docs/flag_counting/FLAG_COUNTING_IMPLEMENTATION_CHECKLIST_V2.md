<!-- CURRENT CANON NOTICE
This file is retained as historical/context documentation. For current Phoenix implementation decisions, use:

docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting Implementation Checklist V2

This checklist converts `FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md` into concrete engineering tasks.

Every item should be treated as an acceptance criterion for the next implementation pass.

---

## 1. Module boundaries

Recommended modules:

```text
FCN_NodeEngine.mqh
FCN_NodeCompression.mqh
FCN_NDDetector.mqh
FCN_FlagGeometry.mqh
FCN_SequenceEngine.mqh
FCN_Renderer.mqh
FCN_Audit.mqh
FlagCountingVNextExperiment.mq5
```

Existing files may be reused, but the internal responsibilities should match these boundaries.

---

## 2. Node engine checklist

### 2.1 High/low only

- [ ] Node extraction uses `high` and `low` only.
- [ ] No structure rule uses `open`.
- [ ] No structure rule uses `close`.
- [ ] No structure rule uses candle body.
- [ ] No structure rule uses candle color.
- [ ] Audit explicitly reports that logic is close-agnostic.

### 2.2 Raw node preservation

- [ ] Raw nodes are preserved.
- [ ] Compressed nodes reference raw node ids.
- [ ] Compression does not delete raw audit information.
- [ ] Every rendered F/ND can report its source raw nodes.

### 2.3 Alternating compressed view

- [ ] Compression can convert raw noisy nodes into an alternating H-L-H-L or L-H-L-H view.
- [ ] Same-side consecutive highs keep the highest high for an upward impulse.
- [ ] Same-side consecutive lows keep the lowest low for a downward impulse.
- [ ] Same-side correction lows keep the lowest low as bullish waist candidate.
- [ ] Same-side correction highs keep the highest high as bearish waist candidate.

---

## 3. ND detector checklist

### 3.1 ND node count

- [ ] Two-node structures are not labeled ND.
- [ ] Three-node structures may be labeled ND.
- [ ] Four-node structures may be labeled ND.
- [ ] More than four nodes trigger adaptive L compression.
- [ ] If still more than four after max L, log unresolved ND candidate.

### 3.2 Adaptive L

- [ ] Source/root L starts at 2.
- [ ] Source/root L is not increased.
- [ ] Local structure L is increased until node count is <= 4.
- [ ] Final L is stored in ND audit fields.

### 3.3 50% cycle threshold

- [ ] Default ND requires >= 50% high/low cycle threshold.
- [ ] Input exists to allow below-50 ND.
- [ ] Ratio is computed from high/low node range only.
- [ ] No candle close participates in the ratio.

Suggested inputs:

```text
InpScanND = true
InpDetectAllND = true
InpNDMinNodes = 3
InpNDMaxNodes = 4
InpNDStartL = 2
InpNDMinCycleRatio = 0.50
InpAllowBelow50ND = false
InpDrawND = true
InpMaxNDPerScale = 250
```

---

## 4. Flag geometry checklist

### 4.1 Common two-leg body

Every F must have:

```text
origin
leg1
waist
leg2
```

- [ ] No rendered F is allowed without all four structural points.
- [ ] Every F has a direction.
- [ ] Every F has a sequence id.
- [ ] Every F has an F level: 1, 2, or 3.
- [ ] Every F has a status: candidate, confirmed, terminal, rejected.

### 4.2 Bullish body

- [ ] Origin is LOW.
- [ ] Leg1 is the highest HIGH before correction.
- [ ] Waist is the lowest LOW in the correction before Leg2.
- [ ] Leg2 is the HIGH that breaks/extends Leg1.
- [ ] If Leg2 extends before post-flag 1/2 appears, update Leg2.

### 4.3 Bearish body

- [ ] Origin is HIGH.
- [ ] Leg1 is the lowest LOW before correction.
- [ ] Waist is the highest HIGH in the correction before Leg2.
- [ ] Leg2 is the LOW that breaks/extends Leg1.
- [ ] If Leg2 extends before post-flag 1/2 appears, update Leg2.

---

## 5. F1 checklist

### 5.1 F1 origin

- [ ] F1 can start after ND.
- [ ] F1 can start after the end context of an opposite F sequence.
- [ ] F1 cannot start from an arbitrary middle node.
- [ ] F1 origin is tagged with source context.

### 5.2 F1 invalidation

- [ ] F1 invalidation is the waist.
- [ ] Bullish F1 invalidates if waist is hit/broken downward.
- [ ] Bearish F1 invalidates if waist is hit/broken upward.
- [ ] Invalidated F1 is not drawn on the main chart.
- [ ] Invalidated F1 is logged.

### 5.3 F1 internal 1/2

- [ ] Internal 1/2 forms after Leg2.
- [ ] Bullish internal 2 is below internal 1.
- [ ] Bearish internal 2 is above internal 1.
- [ ] There is an intervening opposite node between 1 and 2.
- [ ] For F1, the intervening node must not break beyond the F1 flag endpoint.

### 5.4 F1 confirmation

- [ ] F1 confirms only after valid internal 1/2 or compressed equivalent.
- [ ] F1 confirms when price returns and hits/breaks the flag endpoint using high/low geometry.
- [ ] F1 must not confirm from candle close.

---

## 6. F2 checklist

### 6.1 F2 start

- [ ] F2 starts only after F1 confirmation.
- [ ] F2 origin is the terminal/deeper endpoint of F1 post-flag correction.
- [ ] F2 is not created from an unconfirmed F1.

### 6.2 F2 invalidation

- [ ] F2 invalidation is its origin / beginning of Leg1.
- [ ] F2 may break its waist without invalidating.
- [ ] If F2 origin is hit, F2 is rejected.
- [ ] F1 parent remains alive after F2 rejection if F1 remains valid.
- [ ] The system continues searching for F2 from the F1 context.

### 6.3 F2 waist-break branch

- [ ] If F2 breaks waist but not origin, create branch interpretation.
- [ ] Branch internal 1 = F2 waist.
- [ ] Branch internal 2 = node that breaks F2 waist.
- [ ] Branch remains inside F2 context.

### 6.4 F2 confirmation

- [ ] F2 requires post-body internal 1/2 or more.
- [ ] F2 can break waist during this process.
- [ ] F2 cannot hit origin.
- [ ] F2 confirms by breaking flag endpoint after internal 1/2.

### 6.5 F2 size

- [ ] F2 size is measured from origin to Leg2.
- [ ] F2 size must be >= F1 size by default.
- [ ] Size comparison uses price distance only.

---

## 7. F3 checklist

- [ ] F3 starts after F2 context.
- [ ] F3 classification requires only the two-leg flag body.
- [ ] F3 does not require post-body 1/2.
- [ ] When F3 body completes, sequence is locked.
- [ ] Locked sequence is not deleted after later reversal.
- [ ] Further same-direction movement is F3 extension.
- [ ] No F4 is created.
- [ ] Opposite smallest F1 rule is documented as unresolved until formalized.

---

## 8. Sequence engine checklist

### 8.1 State progression

Required states:

```text
NO_SEQUENCE
WAIT_F1
F1_CANDIDATE
F1_CONFIRMED_WAIT_F2
F2_CANDIDATE
F2_CONFIRMED_WAIT_F3
F3_CANDIDATE
F3_LOCKED
```

Optional sub-states:

```text
WAIT_INTERNAL_12
WAIT_ENDPOINT_REBREAK
WAIST_BREAK_BRANCH
EXTENDING_LEG2
```

### 8.2 Parent-child behavior

- [ ] Child invalidation does not kill valid parent.
- [ ] Parent invalidation kills dependent child contexts.
- [ ] Dead child origin is not reused to resurrect the same child.
- [ ] Parent continues searching for the expected next F.

### 8.3 Sequence numbering

- [ ] After F1, next same-sequence flag is F2.
- [ ] After F2, next same-sequence flag is F3.
- [ ] Do not reset to F1 inside the same chain.

---

## 9. Renderer checklist

### 9.1 Main chart visibility

Draw:

```text
candidate F
confirmed F
terminal F3
ND label
origin O label
internal 1/2 labels
```

Do not draw:

```text
rejected F
dead origin
orphan line
invalidated child
```

### 9.2 Labels

- [ ] Detailed label mode C is supported: `F1 L8 Q23`.
- [ ] Origin label `O` is enabled by default.
- [ ] ND label is text-only.
- [ ] Peaks place labels above.
- [ ] Valleys place labels below.
- [ ] Stacking is deterministic.
- [ ] Older sequence is closer to price.

Suggested inputs:

```text
InpShowDetailedLevelLabels = true
InpShowOriginLabels = true
InpShowInternal12Labels = true
InpDrawND = true
InpStackLabels = true
InpOlderSequenceCloserToPrice = true
```

### 9.3 Lines and curves

- [ ] All lines use fixed thin width by default.
- [ ] Sequence identity is shown by shade variation, not thickness.
- [ ] Origin to Leg1 is straight.
- [ ] Leg1 to Leg2 is a smooth curve through waist.
- [ ] Curve uses enough points to avoid visible broken segments.

Suggested inputs:

```text
InpFixedLineWidth = 1
InpUseSequenceColorShades = true
InpCurveSegments = 32
```

---

## 10. Audit checklist

Every event should be able to report:

```text
symbol
timeframe
sequence id
F level
status
direction
scale L
raw source node ids
compressed node ids
origin
leg1
waist
leg2
internal 1
internal 2
size
invalidation level
confirmation level
parent sequence id
reason for candidate
reason for confirmation
reason for rejection
```

For ND:

```text
node count before compression
node count after compression
L used
cycle ratio
accepted below 50 flag
overlaps F flag
```

---

## 11. Regression tests

### 11.1 High/low only test

Create test data where close changes but highs/lows stay identical.

Expected:

```text
F/ND detection must be identical.
```

### 11.2 F1 waist invalidation test

Bullish:

```text
LOW O -> HIGH L1 -> LOW W -> HIGH L2 -> breaks W before confirmation
```

Expected:

```text
F1 rejected
not drawn
logged
```

### 11.3 F2 origin invalidation test

```text
F1 confirmed
F2 candidate
F2 hits origin
```

Expected:

```text
F2 rejected
F1 remains alive
system continues F2 search
```

### 11.4 F3 lock test

```text
F1 -> F2 -> F3 body complete -> full reversal
```

Expected:

```text
F3 remains locked on chart
sequence is not deleted
```

### 11.5 Leg2 extension test

```text
F1 body forms
no internal 1/2
price extends beyond Leg2
```

Expected:

```text
same F1 Leg2 updated
no new fake F created
```

### 11.6 ND compression test

```text
local region has more than 4 raw nodes
increase L until <= 4 readable nodes
```

Expected:

```text
3/4 nodes => ND
2 nodes => not ND
```

---

## 12. Implementation order

Recommended next build order:

```text
1. Freeze this documentation.
2. Implement high/low-only node and compression audit.
3. Implement ND detector separately from F detector.
4. Implement common two-leg flag geometry builder.
5. Implement F1 state machine.
6. Implement F2 state machine with parent continuity.
7. Implement F3 lock and extension logic.
8. Implement renderer after detector outputs are clean.
9. Add audit logs and regression fixtures.
10. Only then reconnect chart visualization at full density.
```

Do not patch renderer repeatedly before the sequence model is correct.
