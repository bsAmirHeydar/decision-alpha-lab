# Phase 55 — Fast Exact F2 Runtime Hotfix

## Problems corrected

1. The prior runtime used the confirmation node anchor as setup age. A swing anchor predates the bar where its right-side L clearance becomes known, so fresh setups could be classified as old and never sent.
2. The prior runtime called the complete multi-scale sequence finalization stack even though this tester needs only F1 and F2.
3. Hook branches were still scanned as internal F1 context despite this profile being explicitly F-only.
4. Terminal Global Variables, global mutexes, timing counters and runtime prints added unnecessary tester overhead.
5. Broker submission relied on a high-level wrapper without an explicit preflight contract.

## Corrections

- exact node-observability bar reconstructed from right-side clearance;
- age zero means the first closed bar on which F2 is actually knowable;
- Hook scan fully disabled;
- per-scale Phoenix F1/F2 construction retained;
- global visual/canonical post-processing skipped;
- direct pending `MqlTradeRequest` with `OrderCheck` then `OrderSend`;
- SL and TP attached to the pending request;
- one-attempt registry moved to memory;
- all custom runtime prints and timing counters removed.
