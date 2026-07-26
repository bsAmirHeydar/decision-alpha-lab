<!-- CURRENT CANON NOTICE
This file is retained as historical/context documentation. For current Phoenix implementation decisions, use:

docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting Implementation Checklist V3

This checklist is for implementing or auditing the Flag Counting V3 contract. Each item should be reviewed before touching detector code.

---

## 1. High/Low Only

- [ ] Detector reads swing high / swing low nodes.
- [ ] F logic does not use candle open.
- [ ] F logic does not use candle close.
- [ ] F logic does not use candle body.
- [ ] F logic does not use candle color.
- [ ] ND logic does not use candle open.
- [ ] ND logic does not use candle close.
- [ ] ND logic does not use candle body.
- [ ] ND logic does not use candle color.
- [ ] Documentation says close is irrelevant, not forbidden.

---

## 2. Raw Node Preservation

- [ ] All raw high/low nodes are stored.
- [ ] Compression does not delete raw nodes.
- [ ] Same-type consecutive HIGH nodes are compressed by keeping the highest high.
- [ ] Same-type consecutive LOW nodes are compressed by keeping the lowest low.
- [ ] Scaled views are alternating.
- [ ] Adaptive L can increase until node count is `<= 4` where needed.

---

## 3. Flag Body Builder

- [ ] Bullish Origin is LOW.
- [ ] Bullish Leg1 is highest HIGH before correction.
- [ ] Bullish Waist is deepest LOW after Leg1 before Leg2.
- [ ] Bullish Leg2 is HIGH breaking Leg1.
- [ ] Bearish Origin is HIGH.
- [ ] Bearish Leg1 is lowest LOW before correction.
- [ ] Bearish Waist is highest HIGH after Leg1 before Leg2.
- [ ] Bearish Leg2 is LOW breaking Leg1.
- [ ] Correction after Leg1 cannot break Origin.
- [ ] Waist updates until Leg2 is hit.
- [ ] Leg2 extends if no valid post-flag internal structure exists and price continues beyond Leg2.

---

## 4. F1

- [ ] F1 starts only after ND/Hook or opposite sequence endpoint.
- [ ] F1 is not created from a random middle of a move.
- [ ] F1 body is shown once probable flag body is hit.
- [ ] F1 post-flag invalidation boundary is Waist.
- [ ] If F1 Waist is hit before internal `1/2` or more, F1 invalidates.
- [ ] Bullish F1 internal `2` is below internal `1`.
- [ ] Bearish F1 internal `2` is above internal `1`.
- [ ] Bullish F1 middle high between 1 and 2 must not exceed F1 Leg2.
- [ ] Bearish F1 middle low between 1 and 2 must not go below F1 Leg2.
- [ ] F1 confirms only after internal `1/2` or more and rebreak of F1 Leg2.
- [ ] F1 with 3/4 post-flag internal nodes gets internal labels and ND label.
- [ ] Two post-flag nodes are not ND.

---

## 5. F2

- [ ] F2 is sought only after F1 confirmation.
- [ ] F2 origin comes from deepest/farthest terminal post-F1 correction node.
- [ ] Bullish F2 origin is deepest LOW of post-F1 correction context.
- [ ] Bearish F2 origin is highest HIGH of post-F1 correction context.
- [ ] F2 size is `abs(F2.Leg2 - F2.Origin)`.
- [ ] Default F2 size rule: `F2.flag_size >= F1.flag_size`.
- [ ] F2 invalidation boundary is F2 Origin/start of Leg1.
- [ ] F2 may break Waist after flag without invalidation if Origin is not broken.
- [ ] F2 waist-break branch creates `1 = Waist`, `2 = node breaking Waist`.
- [ ] F2 confirms only after internal/branch structure and rebreak of F2 Leg2.
- [ ] If F2 Origin is hit, F2 dies but F1 remains alive.
- [ ] After F2 dies, engine still seeks F2 from the same F1 post-flag correction context.

---

## 6. F3

- [ ] F3 is sought only after F2 confirmation.
- [ ] F3 starts from correction after F2 flag.
- [ ] F3 completes by two-leg body only.
- [ ] F3 same-scale condition is OR, not AND.
- [ ] Condition 1: `F3_leg1_L >= ceil(0.80 * F2_leg1_L)`.
- [ ] Condition 2: `F3.flag_size >= 0.70 * F2.flag_size`.
- [ ] If either condition passes, same-scale compatibility passes.
- [ ] After F3 completes, same-direction movement is F3 extension.
- [ ] No F4 is created.
- [ ] F3 locks only on first smallest confirmed opposite F1.
- [ ] F3 does not lock on raw seed or live unconfirmed opposite F1.
- [ ] Locked F3 is never deleted from chart because of later reversal.

---

## 7. ND / Hook

- [ ] ND scans can run anywhere, including inside F structures.
- [ ] ND is text-only by default.
- [ ] ND requires compressed node count 3 or 4.
- [ ] Compressed node count 2 is not ND.
- [ ] Node count > 4 triggers adaptive L increase.
- [ ] ND start anchor is base L=2.
- [ ] ND retracement ratio is computed from high/low node prices only.
- [ ] Formula: `abs(extreme - last) / abs(extreme - start)`.
- [ ] Default threshold is `>= 0.50`.
- [ ] Input exists to allow below-50 ND research mode.
- [ ] If post-flag internal correction has 3 or 4 nodes, number them and add ND label.

---

## 8. Rendering

- [ ] Raw seeds are not drawn.
- [ ] Candidate/live flags are drawn once probable flag body is hit.
- [ ] Confirmed flags are drawn.
- [ ] Locked F3 is drawn.
- [ ] Rejected/invalidated structures are hidden from main chart.
- [ ] All lines are thin equal width by default.
- [ ] Sequence distinction uses shade variation, not line width.
- [ ] Origin label `O` is visible by default.
- [ ] Detailed label option C is default: `F1 L8 Q23`.
- [ ] Peak labels go above peaks.
- [ ] Valley labels go below valleys.
- [ ] Older sequence labels are closest to price in a local stack.
- [ ] Curve is smooth through Waist, not visibly broken trendline segments.
- [ ] Origin -> Leg1 is straight.
- [ ] Leg1 -> Waist -> Leg2 is smooth curve.

---

## 9. Duplicate Handling

- [ ] Duplicate identity uses both time and price.
- [ ] Duplicate identity includes direction, F level, scale, parent sequence, and all body nodes.
- [ ] Same price at different time is not duplicate.
- [ ] Same time at different price is not duplicate.
- [ ] Tiny difference in any identity field means separate sequence.

---

## 10. Audit Logging

For every rejected/invalidated structure, log:

- [ ] sequence id
- [ ] F level
- [ ] direction
- [ ] scale L
- [ ] origin time/price
- [ ] leg1 time/price
- [ ] waist time/price
- [ ] leg2 time/price
- [ ] rejection reason
- [ ] parent sequence id
- [ ] whether raw seed was hidden
- [ ] compression level changes
- [ ] ND retracement ratio if relevant
- [ ] F3 same-scale condition pass/fail

---

## 11. Anti-Regression Tests

### 11.1 No orphan four-node flags

Create a segment with alternating nodes in the middle of an ongoing move.

Expected:

- [ ] no F1 starts unless there is ND/opposite endpoint context.

### 11.2 F1 Leg2 extension

Create F1 body, no internal 1/2, then continuation beyond Leg2.

Expected:

- [ ] Leg2 updates.
- [ ] no fake new F1 is created.

### 11.3 F1 confirmation

Create F1 body, internal 1/2 before Waist, then rebreak Leg2.

Expected:

- [ ] F1 confirms.
- [ ] sequence moves to seeking F2.

### 11.4 F2 dies but F1 lives

Create confirmed F1, then F2 candidate that hits its Origin.

Expected:

- [ ] F2 candidate invalidates.
- [ ] F1 remains alive.
- [ ] engine continues seeking F2 from F1 correction context.

### 11.5 F2 waist-break branch

Create F2 that breaks Waist but not Origin, then rebreaks Leg2.

Expected:

- [ ] F2 does not die.
- [ ] waist-break branch creates 1/2.
- [ ] F2 confirms on Leg2 rebreak.

### 11.6 F3 same-scale OR condition

Create F3 candidate where only Leg1-L condition passes.

Expected:

- [ ] F3 accepted.

Create F3 candidate where only flag-size condition passes.

Expected:

- [ ] F3 accepted.

Create F3 candidate where neither passes.

Expected:

- [ ] F3 rejected as sequence F3.

### 11.7 F3 lock

Create completed F3 and later a small live opposite F1 that invalidates.

Expected:

- [ ] F3 does not lock on unconfirmed opposite F1.

Create completed F3 and later smallest confirmed opposite F1.

Expected:

- [ ] F3 locks.
- [ ] locked F3 remains visible after reversal.

### 11.8 ND retracement

Create 3-node cycle where final node retraces 49%.

Expected default:

- [ ] no ND.

Enable below-half mode.

Expected:

- [ ] ND candidate may appear as research/below-threshold.

Create 3-node cycle where final node retraces 51%.

Expected:

- [ ] ND label appears.
