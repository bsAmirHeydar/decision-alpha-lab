# Hook / ND Implementation Checklist V1

Use this checklist before modifying the Phoenix code.

## 1. Node engine prerequisites

- [ ] Use project L definition.
- [ ] Use candle high/low only.
- [ ] Preserve equal high/low plateau behavior.
- [ ] Treat equality as non-break.
- [ ] Support optional pending active node.
- [ ] Expose node id, time, price, kind, L, confirmed status.

## 2. Hook engine data model

- [ ] Add HookContext model.
- [ ] Add HookBranch model.
- [ ] Store boundary node id.
- [ ] Store active / resolve node id.
- [ ] Store counted same-side node ids.
- [ ] Store branch count.
- [ ] Store retracement ratio.
- [ ] Store adaptive L iteration count.
- [ ] Store ND qualification status.
- [ ] Store pending-node usage.

## 3. Hook origin boundary

- [ ] Low-side Hook finds first older low strictly lower than active low.
- [ ] High-side Hook finds first older high strictly higher than active high.
- [ ] Boundary node is not counted as internal `1`.
- [ ] No bounded Hook is emitted if no boundary exists, unless audit mode requires unbounded diagnostics.

## 4. Branch extraction

- [ ] Extract multiple branches per Hook.
- [ ] Do not limit number of branches.
- [ ] Number branch nodes old-to-new.
- [ ] Permit shared nodes across distinct branch identities.
- [ ] Deduplicate only by exact counted node id list.
- [ ] Do not count opposite-side nodes as branch numbers.

## 5. Adaptive L

- [ ] Start from base L.
- [ ] Build nodes.
- [ ] Build Hook contexts.
- [ ] Build branches.
- [ ] If any branch has more than four counted nodes, increase L.
- [ ] Rebuild everything after L increase.
- [ ] Stop only when every branch has four or fewer counted nodes.
- [ ] Mark unresolved if max L is reached and branch count still exceeds four.

## 6. ND qualification

- [ ] Branch count 1: not ND.
- [ ] Branch count 2: not ND.
- [ ] Branch count 3: ND candidate.
- [ ] Branch count 4: ND candidate.
- [ ] Branch count 5+: not accepted; triggers L escalation.
- [ ] Apply cycle retracement rule.
- [ ] Default threshold is strictly greater than 50%.
- [ ] Do not draw 50% line by default.

## 7. Hook / F1 integration

- [ ] Hook / ND can provide F1 phase boundary.
- [ ] Bullish F1 origin can use low-side Hook floor / lowest low context.
- [ ] Bearish F1 origin can use high-side Hook ceiling / highest high context.
- [ ] Fail-open roots must be tagged as fallback.
- [ ] Fail-open roots must not be confused with Hook-owned roots.

## 8. Renderer

- [ ] Renderer receives Hook events; it does not build Hook branches.
- [ ] Draw Hook arcs in gray.
- [ ] Draw ND label only for qualified ND branch.
- [ ] Draw branch numbers only from emitted counted nodes.
- [ ] Stack labels by cluster.
- [ ] Collapse dense clusters if enabled.
- [ ] Keep audit labels behind explicit debug input.

## 9. Test scenarios

- [ ] Low-side Hook with only 2 counted lows: no ND label.
- [ ] Low-side Hook with 3 counted lows and retracement above 50%: ND label.
- [ ] Low-side Hook with 4 counted lows and retracement above 50%: ND label.
- [ ] Low-side Hook with 5 counted lows: increase L and rebuild.
- [ ] High-side mirror of every low-side test.
- [ ] Multiple branch sequences inside one Hook.
- [ ] Shared resolve node across multiple branches.
- [ ] Pending active node included in live mode.
- [ ] Confirmed-only mode excludes pending node.
- [ ] Label clusters stack cleanly.

## 10. Rejection checks

Reject the patch if:

- [ ] ND appears on every 3/4 raw sliding window.
- [ ] ND appears on 1/2 branches.
- [ ] 5-node branch appears without L escalation.
- [ ] labels overlap heavily in obvious clusters.
- [ ] renderer creates labels not present in emitted events.
- [ ] Hook engine uses close price.
- [ ] equality is treated as break.
