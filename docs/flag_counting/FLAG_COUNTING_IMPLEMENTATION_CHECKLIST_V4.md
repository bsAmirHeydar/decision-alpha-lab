# Flag Counting Implementation Checklist V4

Use this checklist before modifying code.

---

## 1. Node Engine

- [ ] Reuse the existing project node engine.
- [ ] Do not redefine L inside FlagCounting.
- [ ] L means minimum left/right candles that do not reach the candidate high/low price.
- [ ] Equal highs/lows are merged as one plateau node according to existing logic.
- [ ] Equality does not count as break.
- [ ] Nodes do not expire after confirmation.

---

## 2. Data Model

Each node must expose:

- [ ] time
- [ ] price
- [ ] type: high/low
- [ ] L
- [ ] stable node id
- [ ] plateau/merged identity if applicable

Each flag event must expose:

- [ ] sequence id
- [ ] parent sequence id
- [ ] direction
- [ ] F level
- [ ] status
- [ ] origin node
- [ ] leg1 node
- [ ] waist node
- [ ] leg2 node
- [ ] flag size
- [ ] post-flag correction context id
- [ ] internal hook branches
- [ ] invalidation boundary
- [ ] confirmation boundary

---

## 3. F1 Checklist

- [ ] F1 starts only from legal phase boundary.
- [ ] F1 body is drawn only after Leg2 exists.
- [ ] Leg1 is true pre-correction extreme.
- [ ] Waist is true correction extreme before Leg2.
- [ ] If post-Leg2 break happens before valid 1/2, extend Leg2.
- [ ] F1 requires 1/2 or more before confirmation.
- [ ] In F1, pre-1/2 middle opposite node must not pass Leg2.
- [ ] F1 invalidates if Waist is passed before confirmation.
- [ ] F1 confirms when Leg2 is passed after valid 1/2 or more.

---

## 4. F2 Checklist

- [ ] F2 is authorized only after F1 confirmation.
- [ ] F2 origin is backfilled from deepest adverse correction after F1 Leg2.
- [ ] F2 size must be >= F1 size.
- [ ] F2 may remain candidate while size condition is not yet satisfied.
- [ ] F2 invalidates only if its Origin is passed.
- [ ] If candidate F2 dies, keep parent F1 context and rebuild F2 search from that context.
- [ ] F2 may break Waist without invalidating if Origin holds.
- [ ] F2 waist-break branch maps Waist to 1 and the waist-breaking node to 2.
- [ ] F2 confirms when Leg2 is passed after valid post-flag counting/branch.

---

## 5. F3 Checklist

- [ ] F3 is authorized only after F2 confirmation.
- [ ] F3 origin is backfilled from deepest adverse correction after F2 Leg2.
- [ ] F3 body has two legs.
- [ ] F3 does not need post-flag 1/2.
- [ ] F3 completion uses OR same-scale qualification:
  - [ ] Leg1 L ratio condition: F3 Leg1 L >= 0.80 * F2 Leg1 L
  - [ ] OR flag size condition: F3 flag size >= 0.70 * F2 flag size
- [ ] If F3 does not yet qualify, keep candidate and allow extension.
- [ ] Completed F3 extension continues until first confirmed opposite F1.
- [ ] First confirmed opposite F1 locks F3 and starts new opposite chain.
- [ ] Locked F3 is never deleted by later reversal.

---

## 6. Hook/ND Checklist

- [ ] ND is not based on candle close.
- [ ] ND branch nodes are adverse-side numbered nodes.
- [ ] Build hook branches, not just blind sliding windows.
- [ ] Multiple 1 nodes may share one 2.
- [ ] Count from newest backward when needed to identify branches.
- [ ] Number final branches oldest to newest.
- [ ] If any branch has >4 nodes, raise L until max branch count <=4.
- [ ] 2 nodes are not ND.
- [ ] 3 or 4 nodes are ND if they pass the 50% cycle retracement rule.
- [ ] Default requires retraced > 50%.
- [ ] Add input to allow below-half-cycle ND, default false.
- [ ] Draw all ND by default.
- [ ] Add input to restrict ND to open sequence contexts, default false.
- [ ] Render ND as gray arc, not a 50% line.

---

## 7. Boundary Checklist

- [ ] Equality does not count as hit/break.
- [ ] Bullish break requires lower low or higher high strictly beyond boundary.
- [ ] Bearish break requires higher high or lower low strictly beyond boundary.
- [ ] Default epsilon is zero.
- [ ] Keep optional epsilon input if needed for broker/tick issues.

---

## 8. Display Checklist

- [ ] Renderer draws only emitted engine events.
- [ ] No renderer-side structure invention.
- [ ] Lines thin and same width by default.
- [ ] Sequence shades vary inside same color family.
- [ ] Flag curve: Origin->Leg1 straight, Leg1->Leg2 arc through Waist.
- [ ] ND curve: gray arc from start node to formation node.
- [ ] Labels use option C: F-level, L, sequence id.
- [ ] Origin label O on by default.
- [ ] Invalidated/rejected hidden by default.
- [ ] Candidate visible with different color.
- [ ] F1 displayed after full body exists.
- [ ] F2/F3 can show probable seed/Leg1 stage.

---

## 9. Anti-Regression Tests

Create visual/unit tests for:

- [ ] F1 extending Leg2 when no 1/2 exists.
- [ ] F1 invalidating at Waist before confirmation.
- [ ] F2 origin break killing only F2 candidate, not F1 parent.
- [ ] F2 rebuilding from same post-F1 correction context.
- [ ] F2 waist-break branch confirming correctly.
- [ ] F3 waiting for OR qualification instead of rejection.
- [ ] F3 locking on first confirmed opposite F1.
- [ ] ND branch with multiple 1s sharing one 2.
- [ ] ND branch >4 causing L increase.
- [ ] Equal highs/lows not treated as breaks.
- [ ] Duplicate near-identical but not identical sequences still rendered separately.
